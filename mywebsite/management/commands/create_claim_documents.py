from django.core.management.base import BaseCommand
from mywebsite.models import Claim, ClaimDocument, User  # Replace with your app name
from django.core.files.base import ContentFile
from faker import Faker
import random
import io

fake = Faker()

class Command(BaseCommand):
    help = "Generate sample claim documents for existing claims"

    def handle(self, *args, **kwargs):
        claims = Claim.objects.all()
        users = list(User.objects.all())
        if not claims.exists():
            self.stdout.write(self.style.ERROR("❌ No claims found. Create some claims first."))
            return

        document_types = [
            'police_report', 'medical_report', 'repair_estimate',
            'photos', 'receipts', 'death_certificate', 'other'
        ]

        doc_count = 0

        for claim in claims:
            num_docs = random.randint(1, 5)
            selected_types = random.sample(document_types, num_docs)

            for doc_type in selected_types:
                uploaded_by = random.choice(users)

                # Simulate a small dummy file
                file_content = ContentFile(
                    fake.text(max_nb_chars=100).encode('utf-8'),
                    name=f"{doc_type}_{fake.uuid4()[:8]}.txt"
                )

                ClaimDocument.objects.create(
                    claim=claim,
                    document_type=doc_type,
                    file=file_content,
                    description=fake.sentence(nb_words=8),
                    uploaded_by=uploaded_by
                )

                doc_count += 1

        self.stdout.write(self.style.SUCCESS(f"📄 {doc_count} claim documents created successfully."))
