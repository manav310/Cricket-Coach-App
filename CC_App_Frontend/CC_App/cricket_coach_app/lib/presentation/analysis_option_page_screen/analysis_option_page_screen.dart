import 'package:flutter/material.dart';
import '../../core/app_export.dart';
import '../../widgets/app_bar/appbar_leading_image.dart';
import '../../widgets/app_bar/custom_app_bar.dart';
import 'widgets/analysisgrid_item_widget.dart';

class AnalysisOptionPageScreen extends StatelessWidget {
  const AnalysisOptionPageScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: _buildAppBar(context),
        body: LayoutBuilder(
          builder: (context, constraints) {
            return SingleChildScrollView(
              child: ConstrainedBox(
                constraints: BoxConstraints(minHeight: constraints.maxHeight),
                child: IntrinsicHeight(
                  child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: 14.h, vertical: 14.v),
                    child: Column(
                      children: [
                        _buildHeadingAnalysis(context),
                        SizedBox(height: 20.v),
                        Expanded(
                          child: _buildAnalysisOptions(context),
                        ),
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

  Widget _buildHeadingAnalysis(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(8.h),
      decoration: AppDecoration.fillDeepPurple.copyWith(
        borderRadius: BorderRadiusStyle.roundedBorder20,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CustomImageView(
            imagePath: ImageConstant.imgBatBall,
            height: 40.v,
            width: 44.h,
            radius: BorderRadius.circular(20.h),
          ),
          SizedBox(width: 12.h),
          Flexible(
            child: Text(
              "Choose any one analysis to perform",
              style: CustomTextStyles.bodyLargeBlack900,
              textAlign: TextAlign.center,
            ),
          )
        ],
      ),
    );
  }

  Widget _buildAnalysisOptions(BuildContext context) {
    final List<Map<String, dynamic>> analysisOptions = [
      {
        "text": "Batsman Technique &\nPlay style Analysis",
        "image": ImageConstant.imganalysis1,
        "route": AppRoutes.batsmanTechniqueAnalysisButton,
      },
      {
        "text": "Timing Analysis",
        "image": ImageConstant.imganalysis2,
        "route": AppRoutes.timingAnalysisButton,
      },
      {
        "text": "Body Stance\n& Footwork Analysis",
        "image": ImageConstant.imganalysis3,
        "route": AppRoutes.bodyStanceAnalysisButton,
      },
      {
        "text": "Batsman's Running\nSpeed Analysis",
        "image": ImageConstant.imganalysis4,
        "route": AppRoutes.runningSpeedAnalysisButton,
      },
      {
        "text": "Bowling Speed\nAnalysis",
        "image": ImageConstant.imganalysis5,
        "route": AppRoutes.bowlingSpeedAnalysisButton,
      },
      {
        "text": "Ball Placement\nAnalysis",
        "image": ImageConstant.imganalysis6,
        "route": AppRoutes.ballPlacementAnalysisButton,
      }
    ];

    return Column(
      children: [
        for (int i = 0; i < 3; i++)
          Column(
            children: [
              Row(
                children: [
                  Expanded(
                    child: AnalysisgridItemWidget(
                      text: analysisOptions[i * 2]["text"]!,
                      imagePath: analysisOptions[i * 2]["image"]!,
                      onTap: () {
                        Navigator.pushNamed(context, analysisOptions[i * 2]["route"]!);
                      },
                    ),
                  ),
                  SizedBox(width: 16.h),
                  Expanded(
                    child: AnalysisgridItemWidget(
                      text: analysisOptions[i * 2 + 1]["text"]!,
                      imagePath: analysisOptions[i * 2 + 1]["image"]!,
                      onTap: () {
                        Navigator.pushNamed(context, analysisOptions[i * 2 + 1]["route"]!);
                      },
                    ),
                  ),
                ],
              ),
              SizedBox(height: 20.v),
            ],
          ),
      ],
    );
  }

  void onTapIconone(BuildContext context) {
    Navigator.pop(context);
  }
}
