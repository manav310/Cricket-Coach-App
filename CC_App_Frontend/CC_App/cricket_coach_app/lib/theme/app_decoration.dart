import 'package:flutter/material.dart';
import '../core/app_export.dart';

class AppDecoration {
  // Fill decorations
  static BoxDecoration get fillDeepPurple => BoxDecoration(
    color: appTheme.deepPurple50,
  );
  static BoxDecoration get fillWhiteA => BoxDecoration(
    color: appTheme.whiteA700,
  );
  // M decorations
  static BoxDecoration get m3syslightsecondarycontainer => BoxDecoration(
    color: appTheme.deepPurple5001,
  );
}

class BorderRadiusStyle {
  // Rounded borders
  static BorderRadius get roundedBorder20 => BorderRadius.circular(
    20.h,
  );
}
