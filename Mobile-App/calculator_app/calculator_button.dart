import 'package:flutter/material.dart';

class CalculatorButton extends StatelessWidget {
  final String label;
  final VoidCallback onTap;

  const CalculatorButton({
    Key? key,
    required this.label,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Color buttonColor = Colors.teal[800]!;
    if ('+-*/=%'.contains(label)) {
      buttonColor = Colors.pink[800]!;
    } else if ('()'.contains(label)) {
      buttonColor = Colors.blue[700]!;
    } else if (label == 'C' || label == 'DEL') {
      buttonColor = Colors.red[700]!;
    } else if (label == 'ANS') {
      buttonColor = Colors.green[700]!;
    }

    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: buttonColor,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
          padding: const EdgeInsets.all(20),
        ),
        onPressed: onTap,
        child: Text(
          label,
          style: const TextStyle(fontSize: 24, color: Colors.white),
        ),
      ),
    );
  }
}
