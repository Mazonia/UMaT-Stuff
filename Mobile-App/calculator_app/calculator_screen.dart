import 'package:flutter/material.dart';
import 'package:math_expressions/math_expressions.dart';
import 'calculator_button.dart';

class CalculatorScreen extends StatefulWidget {
  const CalculatorScreen({Key? key}) : super(key: key);

  @override
  _CalculatorScreenState createState() => _CalculatorScreenState();
}

class _CalculatorScreenState extends State<CalculatorScreen> {
  String _output = '0';
  String _expression = '';
  String _lastAnswer = '0';
  bool _isNewInput = true;

  void _buttonPressed(String value) {
    setState(() {
      if (_output == 'Error' && value != 'C') {
        _output = '0';
        _expression = '';
      }

      if (value == 'C') {
        _output = '0';
        _expression = '';
        _isNewInput = true;
      } else if (value == 'DEL') {
        if (_output.isNotEmpty) {
          _output = _output.substring(0, _output.length - 1);
          if (_output.isEmpty) _output = '0';
          _expression = _output;
        }
      } else if (value == 'ANS') {
        if (_isNewInput) {
          _output = _lastAnswer;
        } else {
          _output += _lastAnswer;
        }
        _expression = _output;
      } else if (value == '=') {
        try {
          _lastAnswer = _evaluateExpression(_expression);
          _output = _lastAnswer;
          _isNewInput = true;
        } catch (e) {
          _output = 'Error';
        }
      } else {
        if (_isNewInput) {
          if ('+-*/()%'.contains(value)) {
            _output = _lastAnswer + value;
          } else {
            _output = value == '.' ? '0.' : value;
          }
          _isNewInput = false;
        } else {
          if (!(value == '.' && _output.contains('.'))) {
            if ((_output.endsWith(')') && RegExp(r'[0-9.]').hasMatch(value)) ||
                (RegExp(r'[0-9.]').hasMatch(_output) && value == '(')) {
              _output += '*' + value;
            } else {
              _output += value;
            }
          }
        }
        _expression = _output;
      }
    });
  }

  String _evaluateExpression(String expression) {
    try {
      expression = expression.replaceAll('%', '/100');

      // Auto-close brackets if needed
      int openBrackets = '('.allMatches(expression).length;
      int closeBrackets = ')'.allMatches(expression).length;
      expression += ')' * (openBrackets - closeBrackets);

      Parser parser = Parser();
      Expression exp = parser.parse(expression);
      ContextModel cm = ContextModel();
      double eval = exp.evaluate(EvaluationType.REAL, cm);

      // Convert to integer if decimal is .0
      if (eval == eval.toInt()) {
        return eval.toInt().toString();
      }

      return eval.toString();
    } catch (e) {
      return 'Error';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            Container(
              padding: const EdgeInsets.all(20),
              alignment: Alignment.centerRight,
              child: Text(
                _output,
                style: const TextStyle(fontSize: 48, color: Colors.white),
              ),
            ),
            const Divider(color: Colors.white54),
            Expanded(child: _buildButtonGrid()),
          ],
        ),
      ),
    );
  }

  Widget _buildButtonGrid() {
    const buttons = [
      'C', 'DEL', '%', '/',
      '7', '8', '9', '*',
      '4', '5', '6', '-',
      '1', '2', '3', '+',
      'ANS', '0', '.', '=', '(',
      ')'
    ];
    return GridView.builder(
      padding: const EdgeInsets.all(8.0),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 4,
        childAspectRatio: 1.1,
      ),
      itemCount: buttons.length,
      itemBuilder: (context, index) {
        return CalculatorButton(
          label: buttons[index],
          onTap: () => _buttonPressed(buttons[index]),
        );
      },
    );
  }
}
