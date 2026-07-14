import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ApprovalPromptCard, ApprovalRequest } from '../../src/components/copilot/ApprovalPromptCard';

describe('ApprovalPromptCard Interactive Flow', () => {
  const mockRequest: ApprovalRequest = {
    id: 'apr_123',
    action_name: 'update_task',
    policy_tier: 'confirm_first',
    risk_level: 'medium',
    human_summary: 'Update task',
    execution_preview: 'update()',
    expires_at: '2026-07-14T20:00:00Z'
  };

  it('triggers onDecision with true when Allow is clicked', () => {
    const handleDecision = jest.fn();
    render(
      <ApprovalPromptCard
        request={mockRequest}
        token="token_xyz"
        onDecision={handleDecision}
        isProcessing={false}
      />
    );

    const allowBtn = screen.getByText('Allow');
    fireEvent.click(allowBtn);
    expect(handleDecision).toHaveBeenCalledWith(true);
  });

  it('triggers onDecision with false when Deny is clicked', () => {
    const handleDecision = jest.fn();
    render(
      <ApprovalPromptCard
        request={mockRequest}
        token="token_xyz"
        onDecision={handleDecision}
        isProcessing={false}
      />
    );

    const denyBtn = screen.getByText('Deny');
    fireEvent.click(denyBtn);
    expect(handleDecision).toHaveBeenCalledWith(false);
  });

  it('disables buttons and shows applying indicator when processing is active', () => {
    render(
      <ApprovalPromptCard
        request={mockRequest}
        token="token_xyz"
        onDecision={jest.fn()}
        isProcessing={true}
      />
    );

    const denyBtn = screen.getByText('Deny') as HTMLButtonElement;
    expect(denyBtn.disabled).toBe(true);
    expect(screen.getByText('Applying...')).toBeInTheDocument();
  });
});
