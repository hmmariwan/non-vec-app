from flask import Flask, render_template, request

app = Flask(__name__)

# Matrix multiplication function
def matrix_multiply(A, B):
    if not A or not B:
        return None, "Error: Both matrices must be provided."

    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        return None, "Error: The number of columns in A must be equal to the number of rows in B for multiplication."

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result, None  # No error

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission
@app.route('/multiply', methods=['POST'])
def multiply():
    try:
        # Get input matrices from the form
        A = request.form['matrix_a']
        B = request.form['matrix_b']
        
        # Convert input string into lists of lists (2D array), filtering out empty rows
        A = [list(map(int, row.split())) for row in A.splitlines() if row.strip()]
        B = [list(map(int, row.split())) for row in B.splitlines() if row.strip()]
        
        # Call the matrix multiplication function
        result, error = matrix_multiply(A, B)
        
        return render_template('index.html', result=result, error=error)
    except ValueError:
        return render_template('index.html', error="Input Error: Please ensure you enter valid integers.")
    except Exception as e:
        return render_template('index.html', error=f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app.run(debug=True)
