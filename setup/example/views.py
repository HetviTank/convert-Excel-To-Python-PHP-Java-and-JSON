# views.py
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .forms import ExcelUploadForm
import json

class ExcelToJsonView(View):
    template_name = 'excel_to_json.html'

    def get(self, request):
        form = ExcelUploadForm()
        return render(request, self.template_name, {'form': form, 'output_data': None, 'conversion_type': None})

    def post(self, request):
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Get the uploaded file from the form
            excel_file = form.cleaned_data['excel_file']

            # Check which button was clicked
            action = request.POST.get('action', None)

            if action == 'convert':
                # Convert the Excel file based on the selected conversion type
                conversion_type = request.POST.get('conversion_type', None)

                if conversion_type == 'json':
                    # Convert the DataFrame to a JSON object
                    df = pd.read_excel(excel_file)
                    output_data = df.to_json(orient='records')
                elif conversion_type == 'python':
                    # Convert the Excel file to a Python list
                    output_data = self.create_python_list(excel_file)
                elif conversion_type == 'java':
                    # Convert the Excel file to a Java array
                    output_data = self.create_java_array(excel_file)
                elif conversion_type == 'php':
                    # Convert the Excel file to a PHP array
                    output_data = self.create_php_array(excel_file)
                else:
                    # Handle other cases or show an error message
                    output_data = None
                    conversion_type = None

                return render(
                    request,
                    self.template_name,
                    {'form': form, 'output_data': output_data, 'conversion_type': conversion_type}
                )

        return render(request, self.template_name, {'form': form, 'output_data': None, 'conversion_type': None})

    def create_python_list(self, xlsx_file):
        df = pd.read_excel(xlsx_file)

        # Extract values from DataFrame as a list
        data_list = df.values.tolist()

        return data_list

    def create_java_array(self, xlsx_file):
        # Read Excel file using pandas and convert to a Python list
        df = pd.read_excel(xlsx_file)
        data_list = df.values.tolist()

        # Get the number of rows and columns
        num_rows, num_cols = df.shape

        # Generate Java code to initialize a 2D array
        java_code = 'String[] javaArray = {\n'

        for i, row in enumerate(data_list):
            java_code += '    {"' + '", "'.join(str(cell) for cell in row) + '"}'
            if i < num_rows - 1:
                java_code += ','
            java_code += '\n'

        java_code += '};'

        return java_code
    
    def create_php_array(self, xlsx_file):
        # Read Excel file using pandas and convert to a Python list
        df = pd.read_excel(xlsx_file)
        data_list = df.values.tolist()

        # Get the number of rows and columns
        num_rows, num_cols = df.shape

        # Generate PHP code to initialize an array
        php_code = '$phpArray = array(\n'

        for i, row in enumerate(data_list):
            php_code += '    array("' + '", "'.join(str(cell) for cell in row) + '")'
            if i < num_rows - 1:
                php_code += ','
            php_code += '\n'

        php_code += ');'

        return php_code
