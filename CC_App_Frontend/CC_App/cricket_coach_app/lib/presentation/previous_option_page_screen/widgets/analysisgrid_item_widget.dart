import 'package:flutter/material.dart';
import '../../../core/app_export.dart';

class AnalysisgridItemWidget extends StatelessWidget {
  final String text;
  final String imagePath;
  final VoidCallback onTap;

  const AnalysisgridItemWidget({
    super.key,
    required this.text,
    required this.imagePath,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: EdgeInsets.symmetric(vertical: 15.v, horizontal: 10.h),
        decoration: AppDecoration.m3syslightsecondarycontainer.copyWith(
          borderRadius: BorderRadiusStyle.roundedBorder20,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CustomImageView(
              imagePath: imagePath,
              height: 120.adaptSize,
              width: 120.adaptSize,
              fit: BoxFit.contain,
            ),
            SizedBox(height: 20.v),
            Flexible(
              child: Text(
                text,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                textAlign: TextAlign.center,
                style: CustomTextStyles.titleSmallGray900.copyWith(
                  height: 1.43,
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
