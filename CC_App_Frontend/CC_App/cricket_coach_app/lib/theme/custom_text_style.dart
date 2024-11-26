import 'package:flutter/material.dart';
import '../core/app_export.dart';

/// A collection of pre-defined text styles for customizing text appearance,
/// categorized by different font families and weights.
/// Additionally, this class includes extensions on [TextStyle] to easily apply specific font families to text.
class CustomTextStyles {
  // Body text style
  static TextStyle get bodyLargeBlack900 => theme.textTheme.bodyLarge!.copyWith(
    color: appTheme.black900,
    fontSize: 18.fSize,
  );

  // Title text styles
  static TextStyle get titleLargeGray900 => theme.textTheme.titleLarge!.copyWith(
    color: appTheme.gray900,
    fontSize: 20.fSize,
    fontWeight: FontWeight.w400,
  );

  static TextStyle get titleSmallGray900 => theme.textTheme.titleSmall!.copyWith(
    color: appTheme.gray900,
  );
}

// Extension method (moved outside the class)
extension TextStyleExtensions on TextStyle {
  TextStyle get roboto {
    return copyWith(
      fontFamily: 'Roboto',
    );
  }
}
