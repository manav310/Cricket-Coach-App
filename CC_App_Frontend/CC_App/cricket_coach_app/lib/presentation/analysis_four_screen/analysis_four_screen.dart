import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:camera/camera.dart';
import 'package:video_player/video_player.dart';
import '../../widgets/video_recording_screen.dart';
import 'package:logger/logger.dart';
import '../../core/app_export.dart';
import '../../theme/custom_button_style.dart';
import '../../widgets/app_bar/appbar_leading_image.dart';
import '../../widgets/app_bar/custom_app_bar.dart';
import '../../widgets/custom_elevated_button.dart';
import 'dart:convert';

class AnalysisFourScreen extends StatefulWidget {
  const AnalysisFourScreen({super.key});

  @override
  AnalysisFourScreenState createState() => AnalysisFourScreenState();
}

class AnalysisFourScreenState extends State<AnalysisFourScreen> {
  static final Logger logger = Logger();
  String? _videoPath;
  Key _videoPlayerKey = UniqueKey();
  String? _analysisResult;

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: _buildAppBar(context),
        // Use LayoutBuilder to make the layout responsive
        body: LayoutBuilder(
          builder: (context, constraints) {
            return SingleChildScrollView(
              // ConstrainedBox ensures the content takes at least the full screen height
              child: ConstrainedBox(
                constraints: BoxConstraints(minHeight: constraints.maxHeight),
                // IntrinsicHeight allows the column to size based on its children
                child: IntrinsicHeight(
                  child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: 14.h, vertical: 14.v),
                    child: Column(
                      children: [
                        _buildHeadingAnalysis(context),
                        SizedBox(height: 20.v),
                        // Expand the upload section to fill available space
                        Expanded(
                          child: _buildUploadSection(context),
                        ),
                        SizedBox(height: 20.v),
                        _buildAnalyzeButton(context),
                      ],
                    ),
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  // Snack Bar Function
  void showSnackBar(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  // Upload Video Function
  Future<void> uploadVideo(File videoFile) async {
    final fileSize = await videoFile.length();
    const maxSize = 52428800;  // 50MB in bytes

    if (fileSize > maxSize) {
      logger.w('File size exceeds limit');
      showSnackBar('File size exceeds the 50MB limit');
      // Show an error message to the user
      return;
    }

    var uri = Uri.parse('http://172.17.22.194:8000/api/analysis/upload/');
    // For Android Emulator - "http://10.0.2.2:8000/api/analysis/upload/"
    var request = http.MultipartRequest('POST', uri)
      ..files.add(await http.MultipartFile.fromPath('file', videoFile.path));

    try {
      logger.i('Attempting to upload video from path: ${videoFile.path}');
      var response = await request.send();
      if (response.statusCode == 201) {
        logger.i('Video uploaded successfully');
        setState(() {
          _videoPath = videoFile.path;
          _videoPlayerKey = UniqueKey();
        });
        // You might want to show a success message to the user here
      } else {
        logger.w('Failed to upload video. Status code: ${response.statusCode}');
        showSnackBar('Failed to upload video');
        // You might want to show an error message to the user here
      }
    } catch (e) {
      logger.e('Error uploading video', error: e, stackTrace: StackTrace.current);
      showSnackBar('Error uploading video: ${e.toString()}');
      // You might want to show an error message to the user here
    }
  }

  // Analyze Video Function
  Future<void> analyzeVideo(String videoPath) async {
    var uri = Uri.parse('http://172.17.22.194:8000/api/analyze/runningspeed/');
    // For Android Emulator - "http://10.0.2.2:8000/api/analyze/runningspeed/"
    var request = http.MultipartRequest('POST', uri)
      ..files.add(await http.MultipartFile.fromPath('video', videoPath));

    try {
      logger.i('Attempting to analyze video from path: $videoPath');
      var response = await request.send();
      if (response.statusCode == 200) {
        logger.i('Video analyzed successfully');
        final responseBody = await response.stream.bytesToString();
        final jsonResponse = json.decode(responseBody);
        setState(() {
          _analysisResult = jsonResponse['result'] as String;
        });
      } else {
        logger.w('Failed to analyze video. Status code: ${response.statusCode}');
        setState(() {
          _analysisResult = 'Failed to analyze video';
        });
      }
    } catch (e) {
      logger.e('Error analyzing video', error: e, stackTrace: StackTrace.current);
      setState(() {
        _analysisResult = 'Error analyzing video';
      });
    }
  }

  // Build the app bar with a back button
  PreferredSizeWidget _buildAppBar(BuildContext context) {
    return CustomAppBar(
      leadingWidth: 53.h,
      leading: AppbarLeadingImage(
        imagePath: ImageConstant.imgIcon,
        margin: EdgeInsets.only(
          left: 23.h,
          top: 12.v,
          bottom: 13.v,
        ),
        onTap: () {
          onTapIconone(context);
        },
      ),
    );
  }

  // Build the heading analysis section
  Widget _buildHeadingAnalysis(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(8.h),
      decoration: AppDecoration.fillDeepPurple.copyWith(
        borderRadius: BorderRadiusStyle.roundedBorder20,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              CustomImageView(
                imagePath: ImageConstant.imganalysis4,
                height: 40.v,
                width: 44.h,
                radius: BorderRadius.circular(20.h),
              ),
              SizedBox(width: 12.h),
              // Use Expanded to prevent text overflow
              Expanded(
                child: Text(
                  "Batsman's Running Speed Analysis",
                  style: CustomTextStyles.titleSmallGray900,
                ),
              )
            ],
          ),
          SizedBox(height: 16.v),
          Text(
            "It will measure running speeds of both the batsman on pitch and will give the difference between their running speeds to user as analysis result.",
            style: theme.textTheme.bodySmall!.copyWith(height: 1.67),
          )
        ],
      ),
    );
  }

  // Build the upload section with buttons
  Widget _buildUploadSection(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.symmetric(horizontal: 20.h, vertical: 20.v),
      decoration: AppDecoration.fillDeepPurple.copyWith(
        borderRadius: BorderRadiusStyle.roundedBorder20,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            "Upload Video",
            style: theme.textTheme.headlineSmall,
          ),
          SizedBox(height: 24.v),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Use Expanded for buttons to fill available width
              Expanded(
                child: CustomElevatedButton(
                  text: "From Media",
                  leftIcon: Container(
                    margin: EdgeInsets.only(right: 8.h),
                    child: CustomImageView(
                      imagePath: ImageConstant.imgFolder,
                      height: 18.adaptSize,
                      width: 18.adaptSize,
                    ),
                  ),
                  onPressed: () async {
                    File? videoFile = await pickVideoFile();
                    if (videoFile != null) {
                      await uploadVideo(videoFile);
                      // You might want to show a success message to the user here
                    } else {
                      // You might want to show an error message to the user here
                    }
                  },
                ),
              ),
              SizedBox(width: 20.h),
              Expanded(
                child: CustomElevatedButton(
                  text: "Record",
                  leftIcon: Container(
                    margin: EdgeInsets.only(right: 8.h),
                    child: CustomImageView(
                      imagePath: ImageConstant.imgIconDeepPurple500,
                      height: 18.adaptSize,
                      width: 18.adaptSize,
                    ),
                  ),
                  onPressed: () async {
                    final result = await Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const VideoRecordingScreen()),
                    );
                    if (result is Map<String, dynamic> && result['file'] is XFile) {
                      final XFile videoFile = result['file'] as XFile;
                      final String? filePath = result['path'] as String?;

                      await uploadVideo(File(videoFile.path));
                      logger.i('Recorded video uploaded from path: $filePath');
                    } else {
                      logger.w('No valid video file returned from VideoRecordingScreen');
                    }
                  },
                ),
              ),
            ],
          ),
          if (_videoPath != null) ...[
            SizedBox(height: 20.v),
            Text("Preview Video", style: theme.textTheme.titleMedium),
            SizedBox(height: 10.v),
            VideoPlayerWidget(key: _videoPlayerKey, videoPath: _videoPath!),
          ],
          if (_analysisResult != null) ...[
            SizedBox(height: 20.v),
            Text(
              "Results",
              style: theme.textTheme.titleLarge,
            ),
            SizedBox(height: 10.v),
            Text(
              _analysisResult!,
              style: theme.textTheme.bodyMedium,
              textAlign: TextAlign.center,
            ),
          ],
        ],
      ),
    );
  }

  // You'll need to implement this method to pick a video file
  // Implement video picking logic here
  Future<File?> pickVideoFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.video,
        allowMultiple: false,
      );

      if (result != null && result.files.isNotEmpty) {
        return File(result.files.single.path!);
      } else {
        // User canceled the picker
        return null;
      }
    } catch (e) {
      logger.e('Error picking video file', error: e, stackTrace: StackTrace.current);
      return null;
    }
  }

  // Build the analyze button
  Widget _buildAnalyzeButton(BuildContext context) {
    return CustomElevatedButton(
      height: 74.v,
      width: 172.h,
      text: "Analyze Video",
      buttonStyle: CustomButtonStyles.outlineBlackTL36,
      buttonTextStyle: theme.textTheme.titleLarge!,
      onPressed: _videoPath != null
          ? () => analyzeVideo(_videoPath!)
          : null,
    );
  }

  // Navigate back to the previous screen
  void onTapIconone(BuildContext context) {
    Navigator.pop(context);
  }
}

class VideoPlayerWidget extends StatefulWidget {
  final String videoPath;

  const VideoPlayerWidget({super.key, required this.videoPath});

  @override
  VideoPlayerWidgetState createState() => VideoPlayerWidgetState();
}

class VideoPlayerWidgetState extends State<VideoPlayerWidget> {
  late VideoPlayerController _controller;
  bool _isPlaying = false;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.file(File(widget.videoPath))
      ..initialize().then((_) {
        setState(() {});
      })
      ..addListener(() {
        setState(() {
          _isPlaying = _controller.value.isPlaying;
        });
      });
  }

  @override
  Widget build(BuildContext context) {
    return _controller.value.isInitialized
        ? AspectRatio(
      aspectRatio: _controller.value.aspectRatio,
      child: Stack(
        alignment: Alignment.bottomCenter,
        children: <Widget>[
          VideoPlayer(_controller),
          VideoProgressIndicator(_controller, allowScrubbing: true),
          ControlsOverlay(controller: _controller, isPlaying: _isPlaying),
        ],
      ),
    )
        : Container();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}

class ControlsOverlay extends StatelessWidget {
  const ControlsOverlay({super.key, required this.controller, required this.isPlaying});

  final VideoPlayerController controller;
  final bool isPlaying;

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: <Widget>[
        AnimatedSwitcher(
          duration: const Duration(milliseconds: 50),
          reverseDuration: const Duration(milliseconds: 200),
          child: Center(
            child: Icon(
              isPlaying ? Icons.pause : Icons.play_arrow,
              color: Colors.white,
              size: 100.0,
            ),
          ),
        ),
        GestureDetector(
          onTap: () {
            controller.value.isPlaying ? controller.pause() : controller.play();
          },
        ),
      ],
    );
  }
}

