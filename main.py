import kivy
import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from datetime import datetime

class BillingSystemApp(App):
    def build(self):
        self.products = []

        # Layouts
        root = BoxLayout(orientation='vertical')
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        output_layout = ScrollView()

        # Input widgets
        self.date_input = TextInput(hint_text='Date', readonly=True)
        self.product_input = TextInput(hint_text='Product')
        self.category_input = TextInput(hint_text='Category')
        self.price_input = TextInput(hint_text='Price', input_type='number')
        self.quantity_input = TextInput(hint_text='Quantity', input_type='number')
        self.payment_input = TextInput(hint_text='Payment Method')

        # Buttons
        add_button = Button(text='Add', on_press=self.add_product)
        remove_button = Button(text='Remove', on_press=self.remove_product)
        save_button = Button(text='Save', on_press=self.save_to_csv)
        print_button = Button(text='Print', on_press=self.print_bill)

        # Output widget
        self.output_label = Label(text='Products:\n')

        # Add widgets to layouts
        input_layout.add_widget(self.date_input)
        input_layout.add_widget(self.product_input)
        input_layout.add_widget(self.category_input)
        input_layout.add_widget(self.price_input)
        input_layout.add_widget(self.quantity_input)
        input_layout.add_widget(self.payment_input)
        input_layout.add_widget(add_button)
        input_layout.add_widget(remove_button)
        input_layout.add_widget(save_button)
        input_layout.add_widget(print_button)

        output_layout.add_widget(self.output_label)

        root.add_widget(input_layout)
        root.add_widget(output_layout)

        return root

    def add_product(self, instance):
        product = {
            'Date': self.date_input.text if self.date_input.text else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Product': self.product_input.text,
            'Category': self.category_input.text,
            'Price': self.price_input.text,
            'Quantity': self.quantity_input.text,
            'Payment': self.payment_input.text
        }

        self.products.append(product)
        self.update_output()

    def remove_product(self, instance):
        if self.products:
            self.products.pop()
            self.update_output()

    def save_to_csv(self, instance):
        if self.products:
            filename = 'billing_data.csv'
            with open(filename, 'a', newline='') as csvfile:
                fieldnames = ['Date', 'Product', 'Category', 'Price', 'Quantity', 'Payment']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if csvfile.tell() == 0:
                    writer.writeheader()
                for product in self.products:
                    # Increase the width of the 'Date' column
                    product['Date'] = f'{product["Date"]:<30}'
                    writer.writerow(product)


    def print_bill(self, instance):
        bill_text = 'Bill:\n'
        for product in self.products:
            bill_text += f"{product['Product']} - {product['Quantity']} x {product['Price']} - {product['Payment']}\n"
        self.output_label.text = bill_text

    def update_output(self):
        output_text = 'Products:\n'
        for product in self.products:
            output_text += f"{product['Product']} - {product['Quantity']} x {product['Price']} - {product['Payment']}\n"
        self.output_label.text = output_text

if __name__ == '__main__':
    BillingSystemApp().run()
