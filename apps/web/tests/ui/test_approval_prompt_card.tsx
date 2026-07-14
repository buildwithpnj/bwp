import React from 'react';
import { render, screen } from '@testing-library/react';
import { ApprovalPromptCard, ApprovalRequest } from '../../src/components/copilot/ApprovalPromptCard';

// Mock components
jest.mock('../../src/components/copilot/DestructiveActionWarning', () => ({
  DestructiveActionWarning: () => <div data-testid="destructive-warning">Irreversible</div>
}));

jest.mock('../../src/components/copilot/ApprovalDecisionBar', () => ({
  ApprovalDecisionBar: ({ onDecision }: any) => (
    <div data-testid="decision-bar">
      <button onClick={() => onDecision(true)}>Allow</button>
      <button onClick={() => onDecision(false)}>Deny</button>
    </div>
  )
}));

describe('ApprovalPromptCard Component', () => {
  const mockMediumRequest: ApprovalRequest = {
    id: 'apr_123',
    action_name: 'update_task',
    policy_tier: 'confirm_first',
    risk_level: 'medium',
    human_summary: 'Update task details for "Complete Docs"',
    execution_preview: 'db.update(Task).values(status="completed")',
    expires_at: '2026-07-14T20:00:00Z'
  };

  const mockHighRequest: ApprovalRequest = {
    id: 'apr_456',
    action_name: 'delete_note',
    policy_tier: 'destructive_confirmed',
    risk_level: 'high',
    human_summary: 'Delete note "Confidential Notes"',
    execution_preview: 'db.delete(Note).where(id="note_999")',
    expires_at: '2026-07-14T20:00:00Z'
  };

  it('renders medium risk action card with correct content and reversible indicator', () => {
    const handleDecision = jest.fn();
    render(
      <ApprovalPromptCard
        request={mockMediumRequest}
        token="token_xyz"
        onDecision={handleDecision}
        isProcessing={false}
      />
    );

    expect(screen.getByText('Update task details for "Complete Docs"')).toBeInTheDocument();
    expect(screen.getByText('Medium Risk')).toBeInTheDocument();
    expect(screen.getByText('This action is reversible.')).toBeInTheDocument();
    expect(screen.getByText('db.update(Task).values(status="completed")')).toBeInTheDocument();
  });

  it('renders high risk destructive action card with warning alert', () => {
    const handleDecision = jest.fn();
    render(
      <ApprovalPromptCard
        request={mockHighRequest}
        token="token_abc"
        onDecision={handleDecision}
        isProcessing={false}
      />
    );

    expect(screen.getByText('Delete note "Confidential Notes"')).toBeInTheDocument();
    expect(screen.getByText('High Risk')).toBeInTheDocument();
    expect(screen.getByTestId('destructive-warning')).toBeInTheDocument();
  });
});
