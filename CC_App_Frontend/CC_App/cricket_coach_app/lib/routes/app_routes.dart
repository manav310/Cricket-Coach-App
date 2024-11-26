import 'package:flutter/material.dart';

import '../presentation/analysis_five_screen/analysis_five_screen.dart';
import '../presentation/analysis_four_screen/analysis_four_screen.dart';
import '../presentation/analysis_one_screen/analysis_one_screen.dart';
import '../presentation/analysis_option_page_screen/analysis_option_page_screen.dart';
import '../presentation/analysis_six_screen/analysis_six_screen.dart';
import '../presentation/analysis_three_screen/analysis_three_screen.dart';
import '../presentation/analysis_two_screen/analysis_two_screen.dart';

import '../presentation/app_navigation_screen/app_navigation_screen.dart';
import '../presentation/home_page_screen/home_page_screen.dart';

import '../presentation/previous_five_screen/previous_five_screen.dart';
import '../presentation/previous_four_screen/previous_four_screen.dart';
import '../presentation/previous_one_screen/previous_one_screen.dart';
import '../presentation/previous_option_page_screen/previous_option_page_screen.dart';
import '../presentation/previous_six_screen/previous_six_screen.dart';
import '../presentation/previous_three_screen/previous_three_screen.dart';
import '../presentation/previous_two_screen/previous_two_screen.dart';

//import '../presentation/previous_analysis_one_screen/previous_analysis_one_screen.dart';
//import '../presentation/previous_analysis_two_screen/previous_analysis_two_screen.dart'; // ignore_for_file: must_be_immutable

/// ignore_for_file: must_be_immutable
class AppRoutes {
  static const String batsmanTechniqueAnalysisButton = '/analysis_one_screen';
  static const String timingAnalysisButton = '/analysis_two_screen';
  static const String analysisOptionPageButton = '/analysis_option_page_screen';
  static const String bodyStanceAnalysisButton = '/analysis_three_screen';
  static const String runningSpeedAnalysisButton = '/analysis_four_screen';
  static const String bowlingSpeedAnalysisButton = '/analysis_five_screen';
  static const String ballPlacementAnalysisButton = '/analysis_six_screen';

  //static const String previousAnalysisOneButton = '/previous_analysis_one_screen';
  static const String homePageScreen = '/home_page_screen';
  //static const String analysisResultButton = '/previous_analysis_two_screen';

  static const String batsmanTechniquePreviousButton = '/previous_one_screen';
  static const String timingPreviousButton = '/previous_two_screen';
  static const String previousAnalysisButton = '/previous_option_page_screen';
  static const String bodyStancePreviousButton = '/previous_three_screen';
  static const String runningSpeedPreviousButton = '/previous_four_screen';
  static const String bowlingSpeedPreviousButton = '/previous_five_screen';
  static const String ballPlacementPreviousButton = '/previous_six_screen';

  static const String appNavigationScreen = '/app_navigation_screen';
  static const String initialRoute = '/initialRoute';

  static Map<String, WidgetBuilder> routes = {
    batsmanTechniqueAnalysisButton: (context) => const AnalysisOneScreen(),
    timingAnalysisButton: (context) => const AnalysisTwoScreen(),
    analysisOptionPageButton: (context) => const AnalysisOptionPageScreen(),
    bodyStanceAnalysisButton: (context) => const AnalysisThreeScreen(),
    runningSpeedAnalysisButton: (context) => const AnalysisFourScreen(),
    bowlingSpeedAnalysisButton: (context) => const AnalysisFiveScreen(),
    ballPlacementAnalysisButton: (context) => const AnalysisSixScreen(),

    homePageScreen: (context) => const HomePageScreen(),
    //previousAnalysisOneButton: (context) => const PreviousAnalysisOneScreen(),
    //analysisResultButton: (context) {
    //  final args = ModalRoute.of(context)!.settings.arguments as Map<String, String>;
    //  return PreviousAnalysisTwoScreen(
    //    title: args['title']!,
    //    date: args['date']!,
    //  );
    //},

    batsmanTechniquePreviousButton: (context) => const PreviousOneScreen(),
    timingPreviousButton: (context) => const PreviousTwoScreen(),
    previousAnalysisButton: (context) => const PreviousOptionPageScreen(),
    bodyStancePreviousButton: (context) => const PreviousThreeScreen(),
    runningSpeedPreviousButton: (context) => const PreviousFourScreen(),
    bowlingSpeedPreviousButton: (context) => const PreviousFiveScreen(),
    ballPlacementPreviousButton: (context) => const PreviousSixScreen(),

    appNavigationScreen: (context) => const AppNavigationScreen(),
    initialRoute: (context) => const HomePageScreen()
  };
}
