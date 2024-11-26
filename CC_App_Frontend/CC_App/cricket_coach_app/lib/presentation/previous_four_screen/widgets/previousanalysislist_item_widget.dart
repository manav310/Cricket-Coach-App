import 'package:flutter/material.dart';
import '../../../core/app_export.dart';
import '../../../widgets/custom_elevated_button.dart';

class PreviousanalysislistItemWidget extends StatelessWidget {
  final String title;
  final String date;
  final VoidCallback onViewResult;

  const PreviousanalysislistItemWidget({
    super.key,
    required this.title,
    required this.date,
    required this.onViewResult,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(8.h),
      decoration: AppDecoration.fillDeepPurple.copyWith(
        borderRadius: BorderRadiusStyle.roundedBorder20,
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                // Analysis title
                Text(
                  title,
                  style: theme.textTheme.headlineSmall,
                ),
                SizedBox(height: 12.v),
                // Analysis date
                Text(
                  "Date: $date",
                  style: theme.textTheme.bodyLarge,
                )
              ],
            ),
          ),
          // Button to view analysis result
          CustomElevatedButton(
            width: 122.h,
            text: "View Result",
            onPressed: onViewResult,
          )
        ],
      ),
    );
  }
}
