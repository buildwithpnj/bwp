export function useNotificationActions() {
  const triggerAction = async (notificationId: string, actionType: string, payload: any = {}) => {
    try {
      const res = await fetch(`/api/notifications/${notificationId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action_type: actionType, action_payload: payload })
      });
      return res.ok;
    } catch (e) {
      console.error(e);
      return false;
    }
  };

  return { triggerAction };
}
