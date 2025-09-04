#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Pagamento de Mensalidade
Permite o pagamento da mensalidade através de diferentes métodos
"""

import datetime
from enum import Enum
from typing import Dict, List, Optional
import json

class PaymentMethod(Enum):
    CREDIT_CARD = "cartao_credito"
    DEBIT_CARD = "cartao_debito"
    PIX = "pix"
    BANK_SLIP = "boleto"
    PAYPAL = "paypal"

class PaymentStatus(Enum):
    PENDING = "pendente"
    PROCESSING = "processando"
    APPROVED = "aprovado"
    REJECTED = "rejeitado"
    CANCELLED = "cancelado"

class Payment:
    def __init__(self, user_id: str, amount: float, method: PaymentMethod):
        self.payment_id = f"PAY_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.user_id = user_id
        self.amount = amount
        self.method = method
        self.status = PaymentStatus.PENDING
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.transaction_data = {}

    def to_dict(self) -> Dict:
        return {
            "payment_id": self.payment_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "method": self.method.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "transaction_data": self.transaction_data
        }

class PaymentProcessor:
    def __init__(self):
        self.payments: Dict[str, Payment] = {}
        self.monthly_fee = 29.90  # Valor da mensalidade em R$

    def create_payment(self, user_id: str, method: PaymentMethod) -> Payment:
        """Cria um novo pagamento de mensalidade"""
        payment = Payment(user_id, self.monthly_fee, method)
        self.payments[payment.payment_id] = payment
        print(f"💰 Pagamento criado: {payment.payment_id}")
        return payment

    def process_credit_card(self, payment: Payment, card_data: Dict) -> bool:
        """Processa pagamento via cartão de crédito"""
        print(f"🔄 Processando pagamento via cartão de crédito...")
        
        # Simulação de validação do cartão
        required_fields = ["number", "holder_name", "expiry", "cvv"]
        if not all(field in card_data for field in required_fields):
            payment.status = PaymentStatus.REJECTED
            print("❌ Dados do cartão incompletos")
            return False

        # Simulação de processamento
        payment.status = PaymentStatus.PROCESSING
        payment.transaction_data = {
            "card_last_digits": card_data["number"][-4:],
            "holder_name": card_data["holder_name"]
        }
        
        # Simulação de aprovação (90% de chance)
        import random
        if random.random() > 0.1:
            payment.status = PaymentStatus.APPROVED
            print("✅ Pagamento aprovado via cartão de crédito!")
            return True
        else:
            payment.status = PaymentStatus.REJECTED
            print("❌ Pagamento rejeitado pela operadora")
            return False

    def process_pix(self, payment: Payment) -> str:
        """Processa pagamento via PIX"""
        print(f"🔄 Gerando código PIX...")
        
        # Gera código PIX simulado
        import uuid
        pix_code = str(uuid.uuid4())[:32].upper()
        
        payment.status = PaymentStatus.PROCESSING
        payment.transaction_data = {
            "pix_code": pix_code,
            "expires_at": (datetime.datetime.now() + datetime.timedelta(minutes=30)).isoformat()
        }
        
        print(f"📱 Código PIX gerado: {pix_code}")
        print("⏰ Válido por 30 minutos")
        return pix_code

    def process_bank_slip(self, payment: Payment) -> str:
        """Processa pagamento via boleto bancário"""
        print(f"🔄 Gerando boleto bancário...")
        
        # Gera código de barras simulado
        barcode = f"03399{datetime.datetime.now().strftime('%Y%m%d')}000{int(payment.amount * 100):08d}"
        
        payment.status = PaymentStatus.PROCESSING
        payment.transaction_data = {
            "barcode": barcode,
            "due_date": (datetime.datetime.now() + datetime.timedelta(days=3)).isoformat()
        }
        
        print(f"📄 Boleto gerado com código: {barcode}")
        print("📅 Vencimento em 3 dias")
        return barcode

    def check_payment_status(self, payment_id: str) -> Optional[PaymentStatus]:
        """Verifica o status de um pagamento"""
        if payment_id in self.payments:
            return self.payments[payment_id].status
        return None

    def get_payment_history(self, user_id: str) -> List[Payment]:
        """Retorna o histórico de pagamentos do usuário"""
        return [p for p in self.payments.values() if p.user_id == user_id]

    def confirm_pix_payment(self, payment_id: str) -> bool:
        """Simula confirmação de pagamento PIX"""
        if payment_id in self.payments:
            payment = self.payments[payment_id]
            if payment.method == PaymentMethod.PIX and payment.status == PaymentStatus.PROCESSING:
                payment.status = PaymentStatus.APPROVED
                print("✅ Pagamento PIX confirmado!")
                return True
        return False

def main():
    """Interface principal do sistema de pagamento"""
    processor = PaymentProcessor()
    
    print("=" * 50)
    print("🎮 SISTEMA DE PAGAMENTO - MENSALIDADE JOGOS")
    print("=" * 50)
    print(f"💰 Valor da mensalidade: R$ {processor.monthly_fee}")
    print()
    
    # Solicita dados do usuário
    user_id = input("👤 Digite seu ID de usuário: ").strip()
    if not user_id:
        user_id = "user_demo"
    
    print("\n💳 Métodos de pagamento disponíveis:")
    print("1. Cartão de Crédito")
    print("2. Cartão de Débito")
    print("3. PIX")
    print("4. Boleto Bancário")
    print("5. PayPal")
    
    choice = input("\n🔢 Escolha o método (1-5): ").strip()
    
    method_map = {
        "1": PaymentMethod.CREDIT_CARD,
        "2": PaymentMethod.DEBIT_CARD,
        "3": PaymentMethod.PIX,
        "4": PaymentMethod.BANK_SLIP,
        "5": PaymentMethod.PAYPAL
    }
    
    if choice not in method_map:
        print("❌ Opção inválida!")
        return
    
    selected_method = method_map[choice]
    payment = processor.create_payment(user_id, selected_method)
    
    print(f"\n🆔 ID do Pagamento: {payment.payment_id}")
    
    # Processa o pagamento baseado no método escolhido
    if selected_method in [PaymentMethod.CREDIT_CARD, PaymentMethod.DEBIT_CARD]:
        print(f"\n💳 Processando pagamento via {selected_method.value}...")
        
        # Solicita dados do cartão
        card_data = {
            "number": input("🔢 Número do cartão: ").strip(),
            "holder_name": input("👤 Nome do portador: ").strip(),
            "expiry": input("📅 Validade (MM/AA): ").strip(),
            "cvv": input("🔒 CVV: ").strip()
        }
        
        success = processor.process_credit_card(payment, card_data)
        if success:
            print(f"🎉 Mensalidade paga com sucesso!")
            print(f"📧 Comprovante enviado por email")
        
    elif selected_method == PaymentMethod.PIX:
        pix_code = processor.process_pix(payment)
        print(f"\n📱 Use este código no seu app bancário:")
        print(f"🔗 {pix_code}")
        
        # Simula confirmação
        input("\n⏳ Pressione ENTER após realizar o pagamento...")
        processor.confirm_pix_payment(payment.payment_id)
        
    elif selected_method == PaymentMethod.BANK_SLIP:
        barcode = processor.process_bank_slip(payment)
        print(f"\n🏦 Use este código de barras para pagamento:")
        print(f"📊 {barcode}")
        print("💡 Pode ser pago em qualquer banco ou lotérica")
        
    elif selected_method == PaymentMethod.PAYPAL:
        print(f"\n💰 Redirecionando para PayPal...")
        print(f"🔗 Link de pagamento: https://paypal.com/pay/{payment.payment_id}")
        payment.status = PaymentStatus.PROCESSING
    
    # Mostra status final
    print(f"\n📊 Status do pagamento: {payment.status.value}")
    
    # Salva dados do pagamento
    with open(f"/workspace/payment_{payment.payment_id}.json", "w", encoding="utf-8") as f:
        json.dump(payment.to_dict(), f, indent=2, ensure_ascii=False)
    
    print(f"💾 Dados salvos em: payment_{payment.payment_id}.json")

if __name__ == "__main__":
    main()