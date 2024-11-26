import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:logger/logger.dart';

class VideoRecordingScreen extends StatefulWidget {
  const VideoRecordingScreen({super.key});

  @override
  State<VideoRecordingScreen> createState() => _VideoRecordingScreenState();
}

class _VideoRecordingScreenState extends State<VideoRecordingScreen> {
  CameraController? _controller;
  Future<void>? _initializeControllerFuture;
  bool _isRecording = false;
  final Logger _logger = Logger();
  String? _currentVideoPath;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    try {
      final cameras = await availableCameras();
      final firstCamera = cameras.first;

      _controller = CameraController(
        firstCamera,
        ResolutionPreset.medium,
      );

      _initializeControllerFuture = _controller!.initialize();
      setState(() {}); // Trigger a rebuild once the future is assigned
    } catch (e) {
      _logger.e('Error initializing camera', error: e);
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  Future<void> _startVideoRecording() async {
    if (_controller == null || !_controller!.value.isInitialized) {
      _logger.w('Camera controller is not initialized');
      return;
    }

    try {
      await _initializeControllerFuture;

      final Directory appDirectory = await getApplicationDocumentsDirectory();
      final String videoDirectory = '${appDirectory.path}/Videos';
      await Directory(videoDirectory).create(recursive: true);
      _currentVideoPath = '$videoDirectory/${DateTime.now()}.mp4';

      await _controller!.startVideoRecording();
      _logger.i('Started recording video to: $_currentVideoPath');
      setState(() {
        _isRecording = true;
      });
    } catch (e) {
      _logger.e('Error starting video recording', error: e);
    }
  }

  Future<XFile?> _stopVideoRecording() async {
    if (_controller == null || !_controller!.value.isRecordingVideo) {
      return null;
    }

    try {
      final XFile tempFile = await _controller!.stopVideoRecording();
      final File videoFile = File(tempFile.path);
      final File renamedFile = await videoFile.rename(_currentVideoPath!);

      setState(() {
        _isRecording = false;
      });
      _logger.i('Video saved at: ${renamedFile.path}');
      return XFile(renamedFile.path);
    } on CameraException catch (e) {
      _logger.e('Error stopping video recording', error: e);
      return null;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Record Video')),
      body: _initializeControllerFuture == null
          ? const Center(child: CircularProgressIndicator())
          : FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            return Column(
              children: [
                Expanded(
                  child: CameraPreview(_controller!),
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton(
                      onPressed: _isRecording ? null : _startVideoRecording,
                      child: const Text('Start Recording'),
                    ),
                    ElevatedButton(
                      onPressed: _isRecording
                          ? () async {
                        final videoFile = await _stopVideoRecording();
                        if (videoFile != null && context.mounted) {
                          Navigator.of(context).pop({
                            'file': videoFile,
                            'path': _currentVideoPath
                          });
                        }
                      }
                          : null,
                      child: const Text('Stop Recording'),
                    ),
                  ],
                ),
              ],
            );
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else {
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}

