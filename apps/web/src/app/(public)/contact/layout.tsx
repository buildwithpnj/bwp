import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Contact',
  description: 'Book an AI automation build, commission a production-first agentic workflow, or consult on context-aware systems.',
};

export default function ContactLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
