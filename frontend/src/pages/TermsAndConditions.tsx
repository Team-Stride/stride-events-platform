import { APP_TITLE } from "@/const";

/**
 * Terms & Conditions Page
 * 
 * IMPORTANT: This is a placeholder template. Replace with actual legal terms
 * reviewed by your legal team before going live.
 */
export default function TermsAndConditions() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container max-w-4xl py-12">
        <h1 className="text-4xl font-bold mb-8">Terms and Conditions</h1>
        
        <div className="prose prose-slate dark:prose-invert max-w-none space-y-6">
          <p className="text-sm text-muted-foreground">
            Last Updated: November 9, 2025
          </p>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">1. Acceptance of Terms</h2>
            <p>
              By accessing and using the {APP_TITLE} platform ("Platform"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to these Terms and Conditions, please do not use this Platform.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">2. Use of Platform</h2>
            <h3 className="text-xl font-semibold mt-6 mb-3">2.1 Eligibility</h3>
            <p>
              You must be at least 13 years old to register for events on this Platform. If you are under 18 years old, you must have parental or guardian consent to participate in any events.
            </p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">2.2 Account Registration</h3>
            <p>
              You agree to provide accurate, current, and complete information during the registration process and to update such information to keep it accurate, current, and complete.
            </p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">2.3 Prohibited Activities</h3>
            <p>You agree not to:</p>
            <ul className="list-disc pl-6 space-y-2">
              <li>Use the Platform for any unlawful purpose</li>
              <li>Attempt to gain unauthorized access to any portion of the Platform</li>
              <li>Interfere with or disrupt the Platform or servers</li>
              <li>Use any automated system to access the Platform</li>
              <li>Impersonate any person or entity</li>
              <li>Submit false or misleading information</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">3. Event Registration and Participation</h2>
            <h3 className="text-xl font-semibold mt-6 mb-3">3.1 Registration</h3>
            <p>
              Registration for events is subject to availability and may be limited. Registration fees, if applicable, are non-refundable unless the event is canceled by the organizers.
            </p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">3.2 Payment</h3>
            <p>
              All payments must be made through the Platform's designated payment gateway. You agree to provide valid payment information and authorize the Platform to charge the applicable fees.
            </p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">3.3 Event Rules</h3>
            <p>
              Participants must comply with all event-specific rules and guidelines. Failure to comply may result in disqualification without refund.
            </p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">3.4 Cancellation and Refunds</h3>
            <p>
              Event organizers reserve the right to cancel or reschedule events. In case of cancellation, registered participants will be notified and may be eligible for a refund as per the refund policy.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">4. Intellectual Property</h2>
            <p>
              All content on the Platform, including but not limited to text, graphics, logos, images, and software, is the property of {APP_TITLE} or its content suppliers and is protected by intellectual property laws.
            </p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">4.1 User Submissions</h3>
            <p>
              By submitting content to the Platform (including event submissions, projects, or other materials), you grant {APP_TITLE} a worldwide, non-exclusive, royalty-free license to use, reproduce, modify, and display such content for the purpose of operating and promoting the Platform and events.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">5. Privacy and Data Protection</h2>
            <p>
              Your use of the Platform is also governed by our Privacy Policy. By using the Platform, you consent to the collection and use of your information as described in the Privacy Policy.
            </p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">5.1 Minors' Data</h3>
            <p>
              For participants under 18 years of age, we collect only necessary information with parental consent. Parents/guardians have the right to review, delete, or refuse further collection of their child's information.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">6. Disclaimers and Limitation of Liability</h2>
            <h3 className="text-xl font-semibold mt-6 mb-3">6.1 Platform "As Is"</h3>
            <p>
              The Platform is provided on an "as is" and "as available" basis without warranties of any kind, either express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement.
            </p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">6.2 Limitation of Liability</h3>
            <p>
              To the fullest extent permitted by law, {APP_TITLE} shall not be liable for any indirect, incidental, special, consequential, or punitive damages, or any loss of profits or revenues, whether incurred directly or indirectly, or any loss of data, use, goodwill, or other intangible losses.
            </p>
            
            <h3 className="text-xl font-semibold mt-6 mb-3">6.3 Event Participation</h3>
            <p>
              Participation in events is at your own risk. {APP_TITLE} is not responsible for any injury, loss, or damage that may occur during event participation.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">7. Indemnification</h2>
            <p>
              You agree to indemnify, defend, and hold harmless {APP_TITLE}, its officers, directors, employees, and agents from and against any claims, liabilities, damages, losses, and expenses arising out of or in any way connected with your access to or use of the Platform or your violation of these Terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">8. Termination</h2>
            <p>
              We reserve the right to terminate or suspend your access to the Platform immediately, without prior notice or liability, for any reason, including but not limited to breach of these Terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">9. Governing Law and Dispute Resolution</h2>
            <p>
              These Terms shall be governed by and construed in accordance with the laws of India. Any disputes arising out of or relating to these Terms or the Platform shall be resolved through binding arbitration in accordance with the Arbitration and Conciliation Act, 1996.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">10. Changes to Terms</h2>
            <p>
              We reserve the right to modify these Terms at any time. We will notify users of any material changes by posting the new Terms on the Platform and updating the "Last Updated" date. Your continued use of the Platform after such changes constitutes acceptance of the modified Terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mt-8 mb-4">11. Contact Information</h2>
            <p>
              If you have any questions about these Terms and Conditions, please contact us at:
            </p>
            <div className="bg-muted p-4 rounded-lg mt-4">
              <p><strong>Email:</strong> legal@strideahead.in</p>
              <p><strong>Address:</strong> [Your Company Address]</p>
              <p><strong>Phone:</strong> [Your Contact Number]</p>
            </div>
          </section>

          <div className="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 p-4 mt-8">
            <p className="text-sm font-semibold text-yellow-800 dark:text-yellow-200">
              ⚠️ LEGAL NOTICE: This is a placeholder template. Please have your legal team review and customize these terms before going live with your platform.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
