import 'package:flutter/material.dart';
import '../../core/app_export.dart'; // ignore: must_be_immutable

class AppbarLeadingImage extends StatelessWidget {
  final String? imagePath;
  final EdgeInsetsGeometry? margin;
  final VoidCallback? onTap;

  const AppbarLeadingImage({
    super.key,
    this.imagePath,
    this.margin,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: margin ?? EdgeInsets.zero,
        child: CustomImageView(
          imagePath: imagePath ?? '',
          height: 30.adaptSize,
          width: 30.adaptSize,
          fit: BoxFit.contain,
        ),
      ),
    );
  }
}
