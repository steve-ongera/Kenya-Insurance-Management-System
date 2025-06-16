from django.core.management.base import BaseCommand
from mywebsite.models import Payment, Claim, Policy, Customer, User, Commission  # Adjust import path
from decimal import Decimal
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

class Command(BaseCommand):
    help = "Generate random payments and commissions"

    def handle(self, *args, **kwargs):
        customers = list(Customer.objects.all())
        policies = list(Policy.objects.all())
        claims = list(Claim.objects.all())
        users = list(User.objects.filter(is_active=True))
        agents = list(User.objects.filter(user_type='agent'))

        if not customers or not users:
            self.stdout.write(self.style.ERROR("❌ Requires customers and active users to generate payments."))
            return

        payment_methods = ['cash', 'cheque', 'bank_transfer', 'mobile_money', 'card', 'online']
        payment_statuses = ['pending', 'completed', 'failed', 'cancelled', 'refunded']
        payment_types = ['premium', 'claim', 'refund', 'commission']

        num_payments = 100  # Change to your desired number

        for i in range(num_payments):
            payment_type = random.choice(payment_types)
            method = random.choice(payment_methods)
            status = random.choices(payment_statuses, weights=[0.1, 0.7, 0.1, 0.05, 0.05])[0]

            customer = random.choice(customers)
            policy = random.choice(policies) if payment_type in ['premium', 'commission'] else None
            claim = random.choice(claims) if payment_type == 'claim' else None

            amount = Decimal(random.randint(5000, 100000))
            fee = Decimal(random.uniform(0, 100)).quantize(Decimal("0.01"))
            net = (amount - fee).quantize(Decimal("0.01"))
            processed_by = random.choice(users)

            payment = Payment.objects.create(
                payment_reference=f"PMT{100000 + i}",
                payment_type=payment_type,
                payment_method=method,
                status=status,
                policy=policy,
                claim=claim,
                customer=customer,
                amount=amount,
                transaction_fee=fee,
                net_amount=net,
                transaction_id=fake.uuid4(),
                mpesa_receipt=fake.bothify(text='MP###??###') if method == 'mobile_money' else '',
                cheque_number=str(fake.random_number(digits=6)) if method == 'cheque' else '',
                bank_reference=fake.bban() if method == 'bank_transfer' else '',
                payment_date=datetime.now() - timedelta(days=random.randint(0, 90)),
                due_date=None if payment_type != 'premium' else datetime.now().date() + timedelta(days=30),
                processed_by=processed_by
            )

            self.stdout.write(self.style.SUCCESS(f"✅ Created payment: {payment.payment_reference}"))

            # Generate commission if applicable
            if payment_type == 'premium' and policy and policy.agent and status == 'completed':
                rate = policy.product.commission_rate or Decimal("10.00")
                commission_amount = (amount * rate / Decimal("100.00")).quantize(Decimal("0.01"))

                Commission.objects.create(
                    agent=policy.agent,
                    policy=policy,
                    payment=payment,
                    commission_rate=rate,
                    commission_amount=commission_amount,
                    status=random.choice(['calculated', 'approved', 'paid']),
                    payment_date=payment.payment_date.date(),
                    approved_by=random.choice(users)
                )

                self.stdout.write(self.style.SUCCESS(
                    f"➕ Created commission for agent {policy.agent.username}: KES {commission_amount}"
                ))

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Successfully created {num_payments} payments with commissions."))
