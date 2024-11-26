import 'package:flutter/material.dart';
import '../../core/app_export.dart';

class AppNavigationScreen extends StatelessWidget {
  const AppNavigationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        backgroundColor: const Color(0xFFFFFFFF),
        body: SizedBox(
          width: 375.h,
          child: Column(
            children: [
              Container(
                decoration: const BoxDecoration(
                  color: Color(0xFFFFFFFF),
                ),
                child: Column(
                  children: [
                    SizedBox(height: 10.v),
                    Padding(
                      padding: EdgeInsets.symmetric(horizontal: 20.h),
                      child: Text(
                        "App Navigation",
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: const Color(0xFF000000),
                          fontSize: 20.fSize,
                          fontFamily: 'Roboto',
                          fontWeight: FontWeight.w400,
                        ),
                      ),
                    ),
                    SizedBox(height: 10.v),
                    Padding(
                      padding: EdgeInsets.only(left: 20.h),
                      child: Text(
                        "Check your app's UI from the below demo screens of your app.",
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: const Color(0xFF888888),
                          fontSize: 16.fSize,
                          fontFamily: 'Roboto',
                          fontWeight: FontWeight.w400,
                        ),
                      ),
                    ),
                    SizedBox(height: 5.v),
                    Divider(
                      height: 1.v,
                      thickness: 1.v,
                      color: const Color(0xFF000000),
                    )
                  ],
                ),
              ),
              Expanded(
                child: SingleChildScrollView(
                  child: Container(
                    decoration: const BoxDecoration(
                      color: Color(0xFFFFFFFF),
                    ),
                    child: Column(
                      children: [
                        _buildScreenTitle(
                          context,
                          screenTitle: "Analysis_One",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.batsmanTechniqueAnalysisButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Previous_One",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.batsmanTechniquePreviousButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Analysis_Two",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.timingAnalysisButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Previous_Two",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.timingPreviousButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Previous_Option_Page",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.previousAnalysisButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Home_Page",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.homePageScreen),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Analysis_Option_Page",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.analysisOptionPageButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Analysis_Three",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.bodyStanceAnalysisButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Previous_Three",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.bodyStancePreviousButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Analysis_Four",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.runningSpeedAnalysisButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Previous_Four",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.runningSpeedPreviousButton),
                        ),
                        //_buildScreenTitle(
                        //  context,
                        //  screenTitle: "Previous_Analysis_Two",
                        //onTapScreenTitle: () => onTapScreenTitle(
                        //      context, AppRoutes.analysisResultButton),
                        //),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Analysis_Five",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.bowlingSpeedAnalysisButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Previous_Five",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.bowlingSpeedPreviousButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Analysis_Six",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.ballPlacementAnalysisButton),
                        ),
                        _buildScreenTitle(
                          context,
                          screenTitle: "Previous_Six",
                          onTapScreenTitle: () => onTapScreenTitle(
                              context, AppRoutes.ballPlacementPreviousButton),
                        )
                      ],
                    ),
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }

  /// Common widget
  Widget _buildScreenTitle(
      BuildContext context, {
        required String screenTitle,
        Function? onTapScreenTitle,
      }) {
      return GestureDetector(
        onTap: () {
          onTapScreenTitle?.call();
        },
        child: Container(
          decoration: const BoxDecoration(
            color: Color(0xFFFFFFFF),
          ),
          child: Column(
            children: [
              SizedBox(height: 10.v),
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 20.h),
                child: Text(
                  screenTitle,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: const Color(0xFF000000),
                    fontSize: 20.fSize,
                    fontFamily: 'Roboto',
                    fontWeight: FontWeight.w400,
                  ),
                ),
              ),
              SizedBox(height: 10.v),
              SizedBox(height: 5.v),
              Divider(
                height: 1.v,
                thickness: 1.v,
                color: const Color(0xFF888888),
              )
            ],
          ),
        ),
      );
    }

  /// Common click event
  void onTapScreenTitle(
      BuildContext context,
      String routeName,
      ) {
    Navigator.pushNamed(context, routeName);
  }
}
