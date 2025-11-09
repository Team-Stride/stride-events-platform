import { APP_TITLE } from "@/const";

/**
 * Privacy Policy Page
 * 
 * IMPORTANT: This is a placeholder template compliant with GDPR and Indian data protection laws.
 * Replace with actual privacy policy reviewed by your legal team before going live.
 */
export default function PrivacyPolicy() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container max-w-4xl py-12">
        <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
        
        <div className="prose prose-slate dark:prose-invert max-w-none space-y-6">
          <p className="text-sm text-muted-foreground">
            Last Updated: November 9, 2025
          </p>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">1. Introduction</h2>
            <p>
              {APP_TITLE} ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our Platform.
            </p>
            <p>
              This policy applies to all users of the Platform, including students, parents/guardians, schools, and sponsors. We take special care in protecting the privacy of minors (users under 18 years of age).
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">2. Information We Collect</h2>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">2.1 Personal Information</h3>
            <p>We collect the following types of personal information:</p>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Student Information:</strong> Name, email address, phone number, date of birth, school name, grade/class, stream (Science/Commerce/Arts), city, state</li>
              <li><strong>School Information:</strong> School name, contact person name, email, phone number, address, number of students</li>
              <li><strong>Parent/Guardian Information:</strong> Name, email, phone number, relationship to student (for minors)</li>
              <li><strong>Payment Information:</strong> Payment method details (processed securely through third-party payment gateways)</li>
              <li><strong>Event Submissions:</strong> Projects, code, documents, and other materials submitted for events</li>
            </ul>

            <h3 className="text-xl font-semibold mt-6 mb-3">2.2 Automatically Collected Information</h3>
            <p>We automatically collect certain information when you use the Platform:</p>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Usage Data:</strong> Pages visited, time spent, links clicked, features used</li>
              <li><strong>Device Information:</strong> IP address, browser type, operating system, device type</li>
              <li><strong>Cookies and Tracking:</strong> We use cookies and similar technologies to enhance user experience</li>
            </ul>

            <h3 className="text-xl font-semibold mt-6 mb-3">2.3 Information from Third Parties</h3>
            <p>
              We may receive information about you from third parties such as payment processors, authentication services (Stride ID), and analytics providers.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">3. How We Use Your Information</h2>
            <p>We use the collected information for the following purposes:</p>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Event Management:</strong> Process registrations, manage event participation, evaluate submissions</li>
              <li><strong>Communication:</strong> Send event updates, notifications, results, and certificates</li>
              <li><strong>Payment Processing:</strong> Process registration fees and prize disbursements</li>
              <li><strong>Platform Improvement:</strong> Analyze usage patterns, improve features, fix bugs</li>
              <li><strong>Marketing:</strong> Send promotional emails about upcoming events (with opt-out option)</li>
              <li><strong>Legal Compliance:</strong> Comply with legal obligations, resolve disputes, enforce agreements</li>
              <li><strong>Security:</strong> Detect and prevent fraud, abuse, and security incidents</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">4. Protection of Minors' Privacy</h2>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">4.1 Parental Consent</h3>
            <p>
              For users under 18 years of age, we require verifiable parental consent before collecting personal information. Parents/guardians must provide consent during the registration process.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-3">4.2 Limited Data Collection</h3>
            <p>
              We collect only the minimum information necessary for event participation from minors. We do not collect sensitive information such as financial data directly from minors.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-3">4.3 Parental Rights</h3>
            <p>Parents/guardians have the right to:</p>
            <ul className="list-disc pl-6 space-y-2">
              <li>Review the personal information collected from their child</li>
              <li>Request deletion of their child's information</li>
              <li>Refuse to allow further collection or use of their child's information</li>
              <li>Withdraw consent at any time</li>
            </ul>
            <p>
              To exercise these rights, please contact us at privacy@strideahead.in
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">5. How We Share Your Information</h2>
            <p>We may share your information with:</p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">5.1 Service Providers</h3>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Payment Processors:</strong> Razorpay, Stripe (for payment processing)</li>
              <li><strong>Email Service:</strong> SendGrid (for email notifications)</li>
              <li><strong>WhatsApp Service:</strong> Karix (for WhatsApp notifications)</li>
              <li><strong>Cloud Hosting:</strong> AWS, Google Cloud, or similar (for data storage)</li>
              <li><strong>Analytics:</strong> Google Analytics or similar (for usage analysis)</li>
            </ul>

            <h3 className="text-xl font-semibold mt-6 mb-3">5.2 Event Partners and Sponsors</h3>
            <p>
              We may share aggregate, non-personally identifiable information with event sponsors and partners. We will not share personal information without explicit consent.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-3">5.3 Legal Requirements</h3>
            <p>
              We may disclose your information if required by law, court order, or government request, or to protect our rights, property, or safety.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-3">5.4 Business Transfers</h3>
            <p>
              In the event of a merger, acquisition, or sale of assets, your information may be transferred to the acquiring entity.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">6. Data Security</h2>
            <p>
              We implement appropriate technical and organizational measures to protect your personal information:
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Encryption:</strong> Data is encrypted in transit (HTTPS/TLS) and at rest</li>
              <li><strong>Access Controls:</strong> Limited access to personal data on a need-to-know basis</li>
              <li><strong>Secure Storage:</strong> Data stored in secure, industry-standard cloud infrastructure</li>
              <li><strong>Regular Audits:</strong> Periodic security assessments and vulnerability testing</li>
              <li><strong>Incident Response:</strong> Procedures in place to respond to data breaches</li>
            </ul>
            <p>
              However, no method of transmission over the Internet is 100% secure. While we strive to protect your information, we cannot guarantee absolute security.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">7. Data Retention</h2>
            <p>
              We retain your personal information for as long as necessary to fulfill the purposes outlined in this Privacy Policy, unless a longer retention period is required by law.
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Active Users:</strong> Data retained while your account is active</li>
              <li><strong>Event Participants:</strong> Data retained for 3 years after event completion for certificate issuance and historical records</li>
              <li><strong>Payment Records:</strong> Retained for 7 years as required by Indian tax laws</li>
              <li><strong>Marketing Data:</strong> Retained until you opt out or request deletion</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">8. Your Rights</h2>
            <p>You have the following rights regarding your personal information:</p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">8.1 Access and Portability</h3>
            <p>
              You have the right to request a copy of your personal information in a structured, machine-readable format.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-3">8.2 Correction</h3>
            <p>
              You have the right to request correction of inaccurate or incomplete personal information.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-3">8.3 Deletion</h3>
            <p>
              You have the right to request deletion of your personal information, subject to legal obligations and legitimate business needs.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-3">8.4 Opt-Out</h3>
            <p>
              You can opt out of marketing communications at any time by clicking the "unsubscribe" link in emails or contacting us directly.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-3">8.5 Object to Processing</h3>
            <p>
              You have the right to object to certain types of processing, such as direct marketing.
            </p>

            <p className="mt-4">
              To exercise any of these rights, please contact us at privacy@strideahead.in
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">9. Cookies and Tracking Technologies</h2>
            <p>
              We use cookies and similar technologies to enhance your experience on the Platform:
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Essential Cookies:</strong> Required for Platform functionality (authentication, security)</li>
              <li><strong>Analytics Cookies:</strong> Help us understand how users interact with the Platform</li>
              <li><strong>Marketing Cookies:</strong> Used to deliver relevant advertisements</li>
            </ul>
            <p>
              You can control cookies through your browser settings. However, disabling cookies may affect Platform functionality.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">10. International Data Transfers</h2>
            <p>
              Your information may be transferred to and processed in countries other than India. We ensure that such transfers comply with applicable data protection laws and implement appropriate safeguards.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">11. Changes to This Privacy Policy</h2>
            <p>
              We may update this Privacy Policy from time to time. We will notify you of any material changes by posting the new Privacy Policy on the Platform and updating the "Last Updated" date. Your continued use of the Platform after such changes constitutes acceptance of the updated Privacy Policy.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">12. Contact Us</h2>
            <p>
              If you have any questions, concerns, or requests regarding this Privacy Policy or our data practices, please contact us:
            </p>
            <div className="bg-muted p-4 rounded-lg mt-4">
              <p><strong>Privacy Officer</strong></p>
              <p><strong>Email:</strong> privacy@strideahead.in</p>
              <p><strong>Address:</strong> [Your Company Address]</p>
              <p><strong>Phone:</strong> [Your Contact Number]</p>
            </div>
          </section>

          <div className="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 p-4 mt-8">
            <p className="text-sm font-semibold text-yellow-800 dark:text-yellow-200">
              ⚠️ LEGAL NOTICE: This is a placeholder template compliant with GDPR and Indian data protection laws. Please have your legal team review and customize this policy before going live with your platform.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
