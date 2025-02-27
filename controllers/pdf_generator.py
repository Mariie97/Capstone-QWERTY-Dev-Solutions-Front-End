import base64
import io


from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from datetime import date
from utilities import CITIES


class AgreementContract:

    def __init__(self, job_info):
        self.job_info = job_info
        self.buffer = io.BytesIO()
        self.canvas = Canvas(self.buffer, pagesize=letter)
        self.pdf = None

        self.generate_contract()

    def generate_contract(self):
        client_first_name = self.job_info['owner_name']
        client_last_name = self.job_info['owner_last']
        client_name = str(client_first_name) + ' ' + str(client_last_name)

        student_first_name = self.job_info['student_name']
        student_last_name = self.job_info['student_last']
        student_name = str(student_first_name) + ' ' + str(student_last_name)

        job_title = self.job_info['title']
        job_description = self.job_info['description']
        job_street = self.job_info['street']
        job_city = self.job_info['city']
        job_zip = self.job_info['zipcode']
        job_address = job_street + ', ' + CITIES[job_city] + ', Puerto Rico, ' + str(job_zip)
        job_price = self.job_info['price']

        styles = getSampleStyleSheet()
        width, height = letter

        self.canvas.setFont('Helvetica', 10, leading=None)
        self.canvas.drawRightString(width - 0.5 * inch, height - 0.25 * inch, 'Contract Automatically Generated - '
                                    + str(date.today()))

        image = Image('controllers/NewLogo.jpeg')
        image.drawOn(self.canvas, 230, 630)

        self.canvas.setFont('Helvetica', 12, leading=None)
        self.canvas.drawCentredString(width * 0.5, 600, 'Client-Student Contract Agreement for: ')
        self.canvas.setFont('Helvetica-BoldOblique', 15, leading=None)
        self.canvas.drawCentredString(width * 0.5, 580, job_title.upper())

        self.canvas.setFont('Helvetica', 13, leading=None)
        self.canvas.drawString(inch, 535, 'Client: ' + client_name)
        self.canvas.drawString(inch, 518, 'Student: ' + student_name)

        self.canvas.setFont('Helvetica-Bold', 14, leading=None)
        self.canvas.drawString(width * 0.5 - 0.5 * inch, 490, 'Job Details')

        self.canvas.setFont('Helvetica', 13, leading=None)
        style = ParagraphStyle(name='Description', parent=styles['BodyText'], fontName='Helvetica', fontSize=13,
                               leading=15)
        description = Paragraph('Description: ' + job_description, style, bulletText=None)
        description.wrap(width - 2 * inch, 200)
        description.drawOn(self.canvas, inch, 300)
        self.canvas.drawString(inch, 270, 'Location: ' + job_address)
        self.canvas.drawString(inch, 250, 'Price: ' + job_price)

        text = 'This document uses the following terminology: the Student is defined as the party that will complete ' \
               'the job that has been listed, while the Client is the person that posts the job and pays the student.'

        clause = Paragraph(text, style, bulletText=None)
        clause.wrap(width - 2 * inch, 50)
        clause.drawOn(self.canvas, inch, 185)

        text1 = '1. Payment – The client must pay the agreed price, detailed above, upon satisfactory completion ' \
                'of the job by the student. '
        clause1 = Paragraph(text1, style, bulletText=None)
        clause1.wrap(width - 2 * inch, 50)
        clause1.drawOn(self.canvas, inch, 135)

        text2 = '2. Schedule – The student will complete the job in accordance with the agreed upon schedule.'
        clause2 = Paragraph(text2, style, bulletText=None)
        clause2.wrap(width - 2 * inch, 50)
        clause2.drawOn(self.canvas, inch, 85)

        self.canvas.showPage()

        text3 = '3. Entire Agreement - This document reflects the entire agreement between the Parties and reflects ' \
                'a complete understanding of the Parties with respect to the subject matter. This Contract ' \
                'supersedes all prior written and oral representations. The Contract may not be amended, altered, ' \
                'or supplemented except in writing signed by both Parties. '
        clause3 = Paragraph(text3, style, bulletText=None)
        clause3.wrap(width - 2 * inch, 100)
        clause3.drawOn(self.canvas, inch, 665)

        text4 = '4. Legal and Binding Contract - This Contract is legal and binding between the Parties as stated ' \
                'above. This Contract may be entered into and is legal and binding in Puerto Rico, the United ' \
                'States, and its other territories. The Parties each represent that they have the authority to enter ' \
                'into this Contract.'
        clause4 = Paragraph(text4, style, bulletText=None)
        clause4.wrap(width - 2 * inch, 100)
        clause4.drawOn(self.canvas, inch, 580)

        text5 = '5. Severability - If any provision of this Contract shall be held to be invalid or unenforceable ' \
                'for any reason, the remaining provisions shall continue to be valid and enforceable. If the ' \
                'Court finds that any provision of this Contract is invalid or unenforceable, but that by limiting ' \
                'such provision it would become valid and enforceable, then such provision shall be deemed to be ' \
                'written, construed, and enforced as so limited. '
        clause5 = Paragraph(text5, style, bulletText=None)
        clause5.wrap(width - 2 * inch, 100)
        clause5.drawOn(self.canvas, inch, 465)

        text6 = '6. Applicable Law - This Contract shall be governed and construed in accordance with the laws of the' \
                ' state where the Property is located, without giving effect to any conflicts of law’s provisions.'
        clause6 = Paragraph(text6, style, bulletText=None)
        clause6.wrap(width - 2 * inch, 100)
        clause6.drawOn(self.canvas, inch, 400)

        text7 = '7. Termination – Both parties can choose to terminate the contract; continued contract ' \
                'terminations without job completions will be faced with disciplinary action from the QWERTY Dev ' \
                'Solutions Admin team.'
        clause7 = Paragraph(text7, style, bulletText=None)
        clause7.wrap(width - 2 * inch, 100)
        clause7.drawOn(self.canvas, inch, 335)

        text8 = 'PaRapido and the QWERTY Dev Solutions Team is not responsible for the general payment process ' \
                'between both Parties. In case of a breach of contract by either Party – namely, failure of payment ' \
                'by the client or failure of job execution by the student – and the dispute that arises cannot ' \
                'be resolved, then both Parties must resort to appropriate legal action. '
        clause8 = Paragraph(text8, style, bulletText=None)
        clause8.wrap(width - 2 * inch, 100)
        clause8.drawOn(self.canvas, inch, 240)

        text9 = 'The page for the corresponding job contains a two-way certification process, allowing each Party to ' \
                'acknowledge and agree to the contract. BY CERTIFYING THIS STEP ON THE AFOREMENTIONED PAGE, BOTH ' \
                'PARTIES ACKNOWLEDGE HAVING READ AND UNDERSTOOD THIS CONTRACT AND THAT BOTH PARTIES ARE SATISFIED ' \
                'WITH THE TERMS AND CONDITIONS CONTAINED IN THIS CONTRACT. BOTH PARTIES ARE ENTITLED TO A COPY ' \
                'OF THIS CONTRACT.'
        clause9 = Paragraph(text9, style, bulletText=None)
        clause9.wrap(width - 2 * inch, 100)
        clause9.drawOn(self.canvas, inch, 120)

        self.canvas.setFont('Helvetica-Bold', 16, leading=None)
        self.canvas.drawCentredString(width * 0.5, 80, 'QWERTY Dev Solutions')
        self.canvas.setFont('Helvetica', 12, leading=None)
        self.canvas.drawCentredString(width * 0.5, 60, 'Email: parapidopr@gmail.com')

        self.canvas.showPage()
        self.canvas.save()
        self.pdf = base64.b64encode(self.buffer.getvalue())
        self.buffer.close()

    def get_pdf(self):
        return self.pdf
