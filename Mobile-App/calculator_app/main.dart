import 'package:flutter/material.dart';
import 'calculator_screen.dart';

void main() => runApp(const CalculatorApp());

class CalculatorApp extends StatelessWidget {
  const CalculatorApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Beautiful Calculator',
      theme: ThemeData.dark(),
      home: const CalculatorScreen(),
    );
  }
}