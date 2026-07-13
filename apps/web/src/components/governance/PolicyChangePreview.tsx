'use client';

import { GovernancePolicyLog } from '@/hooks/useGovernanceConfig';

interface PolicyChangePreviewProps {
  logs: GovernancePolicyLog[];
}

export function PolicyChangePreview({ logs }: PolicyChangePreviewProps) {
  return (
    <div className="space-y-2">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Policy Revision History Logs</span>
      <div className="border border-border rounded-lg overflow-hidden text-xs">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-muted/40 border-b border-border text-muted-foreground text-[10px]">
              <th className="p-2">Field</th>
              <th className="p-2">Old Value</th>
              <th className="p-2">New Value</th>
              <th className="p-2">Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan={4} className="p-4 text-center text-muted-foreground">
                  No policy changes recorded.
                </td>
              </tr>
            ) : (
              logs.map(log => (
                <tr key={log.id} className="border-b border-border/50 hover:bg-muted/10 last:border-0">
                  <td className="p-2 font-medium text-foreground">{log.field_name}</td>
                  <td className="p-2 text-muted-foreground">{log.old_value}</td>
                  <td className="p-2 text-primary font-medium">{log.new_value}</td>
                  <td className="p-2 text-muted-foreground text-[10px]">
                    {new Date(log.created_at).toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
