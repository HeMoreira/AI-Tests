# orders/forms.py

from django import forms

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(label="Endereço de Entrega", widget=forms.Textarea(attrs={'rows': 3}))
    zip_code = forms.CharField(label="CEP", max_length=10)
    city = forms.CharField(label="Cidade", max_length=100)
    state = forms.CharField(label="Estado", max_length=100)
    country = forms.CharField(label="País", max_length=100, initial="Brasil")

    PAYMENT_METHODS = [
        ('Credit Card', 'Cartão de Crédito'),
        ('Bank Slip', 'Boleto Bancário'),
        ('Pix', 'Pix'),
    ]
    payment_method = forms.ChoiceField(label="Método de Pagamento", choices=PAYMENT_METHODS)

    # Campos de cartão de crédito (apenas para exemplo, NÃO armazene em produção)
    # Em um projeto real, você usaria integrações com gateways de pagamento (Stripe, PagSeguro, MercadoPago)
    card_number = forms.CharField(label="Número do Cartão", max_length=16, required=False)
    card_holder_name = forms.CharField(label="Nome no Cartão", max_length=100, required=False)
    expiration_date = forms.CharField(label="Data de Expiração (MM/AA)", max_length=5, required=False)
    cvv = forms.CharField(label="CVV", max_length=4, required=False)

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        card_number = cleaned_data.get('card_number')
        card_holder_name = cleaned_data.get('card_holder_name')
        expiration_date = cleaned_data.get('expiration_date')
        cvv = cleaned_data.get('cvv')

        # Exemplo de validação simples: se for cartão, requer os campos
        if payment_method == 'Credit Card':
            if not card_number:
                self.add_error('card_number', "Número do cartão é obrigatório para pagamento com cartão de crédito.")
            if not card_holder_name:
                self.add_error('card_holder_name', "Nome no cartão é obrigatório para pagamento com cartão de crédito.")
            if not expiration_date:
                self.add_error('expiration_date', "Data de expiração é obrigatória para pagamento com cartão de crédito.")
            if not cvv:
                self.add_error('cvv', "CVV é obrigatório para pagamento com cartão de crédito.")
        return cleaned_data