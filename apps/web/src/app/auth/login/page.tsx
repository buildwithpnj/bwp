'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function AuthLoginRedirect() {
  const router = useRouter();
  
  useEffect(() => {
    router.replace('/login');
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center font-mono text-xs text-muted-foreground">
      {"Redirecting to secure terminal login..."}
    </div>
  );
}
