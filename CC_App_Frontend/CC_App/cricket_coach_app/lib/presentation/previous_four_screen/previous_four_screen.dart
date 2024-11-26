import 'package:flutter/material.dart';
import '../../core/app_export.dart';
import 'widgets/previousanalysislist_item_widget.dart';

class PreviousFourScreen extends StatelessWidget {
  const PreviousFourScreen({super.key});

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
                // Heading section
                _buildPreviousAnalysisHeading(context),
                SizedBox(height: 70.v),
                // List of previous analyses
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
            imagePath: ImageConstant.imganalysis4,
            height: 40.v,
            width: 44.h,
            radius: BorderRadius.circular(20.h),
          ),
          SizedBox(width: 12.h),
          Expanded(
            child: Padding(
              padding: EdgeInsets.only(bottom: 6.v),
              child: Text(
                "View Results of Batsman's Running Speed Analysis",
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
    final analyses = [
      {"title": "Analysis 1", "date": "10th July 2024"},
      {"title": "Analysis 2", "date": "13th July 2024"},
      {"title": "Analysis 3", "date": "14th July 2024"},
    ];

    return ListView.separated(
      physics: const NeverScrollableScrollPhysics(),
      shrinkWrap: true,
      separatorBuilder: (context, index) {
        return SizedBox(height: 28.v);
      },
      itemCount: analyses.length,
      itemBuilder: (context, index) {
        return PreviousanalysislistItemWidget(
          title: analyses[index]["title"]!,
          date: analyses[index]["date"]!,
          onViewResult: () {
            // Functionality related to "View Result" Button
          },
        );
      },
    );
  }

  // Navigation function to go back to the previous screen
  void onTapImgIconone(BuildContext context) {
    Navigator.pop(context);
  }
}
