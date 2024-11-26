import 'package:flutter/material.dart';
import '../../core/app_export.dart';
import '../../../widgets/custom_elevated_button.dart';
import '../../../theme/custom_button_style.dart';

class HomePageScreen extends StatelessWidget {
  const HomePageScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: LayoutBuilder(
          builder: (context, constraints) {
            return SingleChildScrollView(
              child: ConstrainedBox(
                constraints: BoxConstraints(minHeight: constraints.maxHeight),
                child: IntrinsicHeight(
                  child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: 14.h, vertical: 14.v),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Flexible(
                                child: CustomImageView(
                                  imagePath: ImageConstant.imgLogo,
                                  height: 172.adaptSize,
                                  width: 172.adaptSize,
                                ),
                              ),
                              SizedBox(height: 16.v),
                              Text(
                                "Welcome to Cricket Coach",
                                style: theme.textTheme.headlineSmall,
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                        ),
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

  Widget _buildAnalysisOptions(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Flexible(
          child: _buildAnalysisOption(
            context,
            "Start New Analysis",
                () {
              // Add onTap functionality for Start New Analysis
                //Navigate to the analysis option page
                Navigator.pushNamed(context, AppRoutes.analysisOptionPageButton);
            },
          ),
        ),
        SizedBox(height: 20.v),
        Flexible(
          child: _buildAnalysisOption(
            context,
            "View Previous Analysis",
                () {
              // Add onTap functionality for View Previous Analysis
                // Navigate to the analysis option page
                Navigator.pushNamed(context, AppRoutes.previousAnalysisButton);
            },
          ),
        ),
      ],
    );
  }

  Widget _buildAnalysisOption(BuildContext context, String title, VoidCallback onTap) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.symmetric(vertical: 20.v),
      decoration: AppDecoration.fillDeepPurple.copyWith(
        borderRadius: BorderRadiusStyle.roundedBorder20,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            title,
            style: theme.textTheme.titleLarge,
            textAlign: TextAlign.center,
          ),
          SizedBox(height: 10.v),
          CustomElevatedButton(
            height: 44.v,
            width: 114.h,
            text: "Click Here",
            buttonStyle: CustomButtonStyles.outlineBlackTL22,
            onPressed: onTap,
          )
        ],
      ),
    );
  }
}
