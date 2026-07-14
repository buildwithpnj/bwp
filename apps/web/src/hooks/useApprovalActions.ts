import { useState } from 'react';
import { api } from '@/lib/api';

export function useApprovalActions() {
  const [isProcessing, setIsProcessing] = useState(false);

  const decideApproval = async (approvalId: string, approve: boolean, token: string) => {
    setIsProcessing(true);
    try {
      const data = await api<any>(`/api/copilot/approve?approval_id=${approvalId}`, {
        method: 'POST',
        body: {
          approve,
          token
        }
      });
      return { success: true, data };
    } catch (e: any) {
      console.error("Failed to submit approval choice:", e);
      return { success: false, error: e?.message || "Connection failure during action approval" };
    } finally {
      setIsProcessing(false);
    }
  };

  return {
    decideApproval,
    isProcessing
  };
}
