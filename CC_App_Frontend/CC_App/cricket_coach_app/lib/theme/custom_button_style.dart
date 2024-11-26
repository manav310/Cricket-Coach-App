import 'package:flutter/material.dart';
import '../core/app_export.dart';

/// A class that offers pre-defined button styles for customizing button appearance.
class CustomButtonStyles {
  //Outline button style
  static ButtonStyle get outlineBlackTL22 => ElevatedButton.styleFrom(
        backgroundColor: appTheme.deepPurple500.withOpacity(0.08),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(22.h),
        ),
        shadowColor: appTheme.black900.withOpacity(0.15),
        elevation: 2,
      );
  static ButtonStyle get outlineBlackTL36 => ElevatedButton.styleFrom(
        backgroundColor: appTheme.deepPurple500.withOpacity(0.08),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(36.h),
        ),
        shadowColor: appTheme.black900.withOpacity(0.15),
        elevation: 2,
      );
// text button style
  static ButtonStyle get none => ButtonStyle(
          backgroundColor: WidgetStateProperty.all<Color>(Colors.transparent),
          elevation: WidgetStateProperty.all<double>(0),
          side: WidgetStateProperty.all<BorderSide>(
              const BorderSide(color: Colors.transparent)));
}
