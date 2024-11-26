import 'package:flutter/material.dart';
import '../../../core/app_export.dart';
import '../../../theme/custom_button_style.dart';
import '../../../widgets/custom_elevated_button.dart'; // ignore: must_be_immutable

class AnalysisoptionsItemWidget extends StatelessWidget {
  const AnalysisoptionsItemWidget({super.key});

  /// Build Method UI of Widget
  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.maxFinite,
      padding: EdgeInsets.symmetric(vertical: 34.v),
      decoration: AppDecoration.fillDeepPurple.copyWith(
        borderRadius: BorderRadiusStyle.roundedBorder20,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            "Start New Analysis",
            style: theme.textTheme.headlineSmall,
          ),
          SizedBox(height: 20.v),
          CustomElevatedButton(
            height: 44.v,
            width: 114.h,
            text: "Click Here",
            buttonStyle: CustomButtonStyles.outlineBlackTL22,
          )
        ],
      ),
    );
  }
}
