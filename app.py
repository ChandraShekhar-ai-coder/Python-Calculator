from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = ""
    error = ""
    
    if request.method == 'POST':
        try:
            num1_str = request.form.get('num1', '').strip()
            num2_str = request.form.get('num2', '').strip()
            operation = request.form.get('operation')

            # Validate input for operations that require numbers
            if operation != 'sqrt' and (not num1_str or not num2_str):
                error = "Please enter both numbers."
            elif operation == 'sqrt' and not num1_str:
                error = "Please enter the first number."
            else:
                num1 = float(num1_str) if num1_str else 0.0
                num2 = float(num2_str) if num2_str else 0.0

                # Perform the selected simple math operation
                if operation == 'add':
                    res = num1 + num2
                elif operation == 'subtract':
                    res = num1 - num2
                elif operation == 'multiply':
                    res = num1 * num2
                elif operation == 'divide':
                    if num2 == 0:
                        raise ZeroDivisionError("Cannot divide by zero.")
                    res = num1 / num2
                elif operation == 'power':
                    # Restrict exponents to simple integers for fifth-grade math sanity
                    if num2 > 10 or num2 < 0 or not num2.is_integer():
                        error = "Exponent must be a simple positive whole number (0-10)."
                        return render_template('index.html', result=result, error=error)
                    res = math.pow(num1, int(num2))
                elif operation == 'sqrt':
                    if num1 < 0:
                        error = "Square root of a negative number is not allowed."
                        return render_template('index.html', result=result, error=error)
                    res = math.sqrt(num1)
                else:
                    error = "Invalid Operation."
                    return render_template('index.html', result=result, error=error)

                # Clean up display (remove .0 if it's a whole number)
                if res.is_integer():
                    result = int(res)
                else:
                    result = round(res, 4)

        except ZeroDivisionError as e:
            error = str(e)
        except ValueError:
            error = "Invalid input! Please enter numbers only."
        except Exception:
            error = "An error occurred calculation."

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)