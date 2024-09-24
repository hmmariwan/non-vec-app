from flask import Flask, render_template, request

app = Flask(__name__)

# Matrix addition function
def matrix_add(A, B):
    if not A or not B:
        return None, "Error: Both matrices must be provided."
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return None, "Error: Matrices must have the same dimensions for addition."
    
    result = [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    return result, None

# Matrix subtraction function
def matrix_subtract(A, B):
    if not A or not B:
        return None, "Error: Both matrices must be provided."
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return None, "Error: Matrices must have the same dimensions for subtraction."
    
    result = [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    return result, None

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
    
    return result, None

# Scalar multiplication function (with matrix selection)
def scalar_multiply(scalar, matrix):
    if not matrix:
        return None, "Error: Matrix must be provided."
    
    result = [[scalar * matrix[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]
    return result, None

# Matrix transpose function
def matrix_transpose(A):
    if not A:
        return None, "Error: Matrix A must be provided."
    
    result = [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
    return result, None

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission
@app.route('/operate', methods=['POST'])
def operate():
    try:
        # Get input matrices and scalar from the form
        A = request.form.get('matrix_a')
        B = request.form.get('matrix_b')
        scalar = request.form.get('scalar')
        matrix_for_scalar = request.form.get('matrix_for_scalar')  # A or B
        operation = request.form.get('operation')

        # Convert input string into lists of lists (2D array)
        if A:
            A = [list(map(int, row.split())) for row in A.splitlines() if row.strip()]
        if B:
            B = [list(map(int, row.split())) for row in B.splitlines() if row.strip()]

        result, error = None, None
        
        # Perform the chosen operation
        if operation == 'add':
            result, error = matrix_add(A, B)
        elif operation == 'subtract':
            result, error = matrix_subtract(A, B)
        elif operation == 'multiply':
            result, error = matrix_multiply(A, B)
        elif operation == 'scalar_multiply':
            scalar = int(scalar)  # Convert scalar input to integer
            matrix = A if matrix_for_scalar == 'A' else B
            result, error = scalar_multiply(scalar, matrix)
        elif operation == 'transpose':
            result, error = matrix_transpose(A)

        if error:
            return render_template('error.html', error=error)
        return render_template('result.html', result=result)
    
    except ValueError:
        return render_template('error.html', error="Input Error: Please ensure you enter valid integers.")
    except Exception as e:
        return render_template('error.html', error=f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app.run(debug=True)
