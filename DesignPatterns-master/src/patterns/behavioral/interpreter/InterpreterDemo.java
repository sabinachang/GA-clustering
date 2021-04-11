package patterns.behavioral.interpreter;


import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

import patterns.behavioral.interpreter.interpreter.Number;
import patterns.behavioral.interpreter.interpreter.Operand;
import patterns.behavioral.interpreter.interpreter.Variable;
import patterns.behavioral.interpreter.interpreter.Expression;

public class InterpreterDemo {
	
	public static boolean precedence(char a, char b) {
        String high = "*/", low = "+-";
        if (a == '(') {
            return false;
        }
        if (a == ')' && b == '(') {
            System.out.println(")-(");
            return false;
        }
        if (b == '(') {
            return false;
        }
        if (b == ')') {
            return true;
        }
        if (high.indexOf(a) >  - 1 && low.indexOf(b) >  - 1) {
            return true;
        }
        if (high.indexOf(a) >  - 1 && high.indexOf(b) >  - 1) {
            return true;
        }
        //no inspection RedundantIfStatement
        if (low.indexOf(a) >  - 1 && low.indexOf(b) >  - 1) {
            return true;
        }
        return false;
    }


    public static double processPostfix(String postfix, Map <String, Integer> map) {
        Stack<Double> stack = new Stack<>();
        String operations = "+-*/";
        String[] tokens = postfix.split(" ");
        for (String token : tokens) {
            // If token is a number or variable
            if (operations.indexOf(token.charAt(0)) == -1) {
                double term;
                try {
                    term = Double.parseDouble(token);
                } catch (NumberFormatException ex) {
                    term = map.get(token);
                }
                stack.push(term);

                // If token is an operator
            } else {
                double b = stack.pop(), a = stack.pop();
                if (token.charAt(0) == '+') {
                    a = a + b;
                }
                if (token.charAt(0) == '-') {
                    a = a - b;
                }
                if (token.charAt(0) == '*') {
                    a = a * b;
                }
                if (token.charAt(0) == '/') {
                    a = a / b;
                }
                stack.push(a);
            }
        }
        return stack.pop();
    }

    public static String convertToPostfix(String expr) {
        Stack<Character> operationsStack = new Stack<>();
        StringBuilder out = new StringBuilder();
        String operations = "+-*/()";
        char topSymbol = '+';
        boolean empty;
        String[] tokens = expr.split(" ");
        for (String token : tokens)
            if (operations.indexOf(token.charAt(0)) == -1) {
                out.append(token);
                out.append(' ');
            } else {
                while (!(empty = operationsStack.isEmpty()) && precedence(topSymbol =
                        operationsStack.pop(), token.charAt(0))) {
                    out.append(topSymbol);
                    out.append(' ');
                }
                if (!empty) {
                    operationsStack.push(topSymbol);
                }
                if (empty || token.charAt(0) != ')') {
                    operationsStack.push(token.charAt(0));
                } else {
                    topSymbol = operationsStack.pop();
                }
            }
        while (!operationsStack.isEmpty()) {
            out.append(operationsStack.pop());
            out.append(' ');
        }
        return out.toString();
    }

    public static Operand buildSyntaxTree(String tree) {
        Stack <Operand> stack = new Stack<>();
        String operations = "+-*/";
        String[] tokens = tree.split(" ");
        for (String token : tokens)
            if (operations.indexOf(token.charAt(0)) == -1) {
                Operand term;
                try {
                    term = new Number(Double.parseDouble(token));
                } catch (NumberFormatException ex) {
                    term = new Variable(token);
                }
                stack.push(term);

                // If token is an operator
            } else {
                Expression expr = new Expression(token.charAt(0));
                expr.right = stack.pop();
                expr.left = stack.pop();
                stack.push(expr);
            }
        return stack.pop();
    }

    public static void main(String[] args) {
        System.out.println("celsius * 9 / 5 + thirty");
        String postfix = convertToPostfix("celsius * 9 / 5 + thirty");
        System.out.println(postfix);
        Operand expr = buildSyntaxTree(postfix);
        expr.traverse(1);
        System.out.println();
        HashMap < String, Integer > map = new HashMap<>();
        map.put("thirty", 30);
        for (int i = 0; i <= 100; i += 10) {
            map.put("celsius", i);
            System.out.println("C is " + i + ",  F is " + expr.evaluate(map));
        }
    }
}
