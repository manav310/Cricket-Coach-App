import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';
import 'package:intl/intl.dart';
import 'package:path_provider/path_provider.dart';
import 'package:open_file/open_file.dart';
import 'package:logger/logger.dart';
import '../../core/app_export.dart';
import 'widgets/previousanalysislist_item_widget.dart';

class PreviousThreeScreen extends StatefulWidget {
  const PreviousThreeScreen({super.key});

  @override
  PreviousThreeScreenState createState() => PreviousThreeScreenState();
}

class PreviousThreeScreenState extends State<PreviousThreeScreen> {
  static final Logger logger = Logger();
  List<Map<String, dynamic>> analyses = [];

  @override
  void initState() {
    super.initState();
    fetchPreviousAnalyses();
  }

  // Fetching Previous Analysis
  Future<void> fetchPreviousAnalyses() async {
    try {
      final response = await http.get(Uri.parse('http://172.17.22.194:8000/api/previous/bodystance/'));
      // For Android Emulator - "http://10.0.2.2:8000/api/previous/bodystance/"
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        setState(() {
          analyses = List<Map<String, dynamic>>.from(data);
        });
      } else {
        // Handle error
        logger.w('Failed to fetch previous analyses. Status code: ${response.statusCode}');
      }
    } catch (e) {
      // Handle exception
      logger.e('Error fetching previous analyses', error: e, stackTrace: StackTrace.current);
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        // SingleChildScrollView makes the entire screen scrollable
        body: SingleChildScrollView(
          child: Container(
            width: double.maxFinite,
            padding: EdgeInsets.only(
              left: 14.h,
              top: 90.v,
              right: 14.h,
              bottom: 20.v,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Back button
                CustomImageView(
                  imagePath: ImageConstant.imgIcon,
                  height: 30.adaptSize,
                  width: 30.adaptSize,
                  margin: EdgeInsets.only(left: 8.h),
                  onTap: () {
                    onTapImgIconone(context);
                  },
                ),
                SizedBox(height: 6.v),
                _buildPreviousAnalysisHeading(context),
                SizedBox(height: 70.v),
                _buildPreviousAnalysisList(context)
              ],
            ),
          ),
        ),
      ),
    );
  }

  // Widget for the heading section
  Widget _buildPreviousAnalysisHeading(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: 16.h,
        vertical: 8.v,
      ),
      decoration: AppDecoration.fillDeepPurple.copyWith(
        borderRadius: BorderRadiusStyle.roundedBorder20,
      ),
      width: double.maxFinite,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CustomImageView(
            imagePath: ImageConstant.imganalysis3,
            height: 40.v,
            width: 44.h,
            radius: BorderRadius.circular(20.h),
          ),
          SizedBox(width: 12.h),
          Expanded(
            child: Padding(
              padding: EdgeInsets.only(bottom: 6.v),
              child: Text(
                "View Results of Body Stance & Footwork Analysis",
                style: CustomTextStyles.bodyLargeBlack900,
              ),
            ),
          )
        ],
      ),
    );
  }

  // Widget for the list of previous analyses
  Widget _buildPreviousAnalysisList(BuildContext context) {
    return ListView.separated(
      physics: const NeverScrollableScrollPhysics(),
      shrinkWrap: true,
      separatorBuilder: (context, index) {
        return SizedBox(height: 28.v);
      },
      itemCount: analyses.length,
      itemBuilder: (context, index) {
        // Convert the timestamp to a formatted date string
        String formattedDate = DateFormat('yyyy-MM-dd HH:mm:ss').format(
            DateTime.fromMillisecondsSinceEpoch(
                (analyses[index]["date"] as double).toInt() * 1000
            )
        );
        return PreviousanalysislistItemWidget(
          title: "Analysis ${index + 1}",
          date: formattedDate,
          onViewResult: () => downloadPDF(analyses[index]["pdf_id"]),
        );
      },
    );
  }

  // Download PDF
  Future<void> downloadPDF(String pdfId) async {
    try {
      logger.i('Attempting to download PDF with ID: $pdfId');
      final response = await http.get(Uri.parse('http://172.17.22.194:8000/api/download/pdf-bodystance/$pdfId'));
      if (response.statusCode == 200) {
        final bytes = response.bodyBytes;
        final tempDir = await getTemporaryDirectory();
        final file = File('${tempDir.path}/analysis_$pdfId.pdf');
        await file.writeAsBytes(bytes);
        logger.i('PDF downloaded successfully. Opening file: ${file.path}');
        await OpenFile.open(file.path);
      } else {
        // Handle error
        logger.w('Failed to download PDF. Status code: ${response.statusCode}');
      }
    } catch (e) {
      // Handle exception
      logger.e('Error downloading PDF', error: e, stackTrace: StackTrace.current);
    }
  }

  // Navigation function to go back to the previous screen
  void onTapImgIconone(BuildContext context) {
    logger.i('Navigating back to previous screen');
    Navigator.pop(context);
  }
}