"use client";
import { Edit } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { useRouter } from "next/navigation";
import { useState } from "react";

export function StartNewSessionButton () {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function handleCreateNewSession ()
    {
        setError(null);
        setLoading(true);

        // Create Explainatyion Session UI
        // Start websocket
        // After successfull startup from api
        // Render Gracefully.

        setLoading(false);
        router.push("/explaination-session");
    }

    return(
        <div className="space-y-2">
            <Button type="button" variant="secondary" onClick={handleCreateNewSession} disabled={loading}>
                <Edit className="w-4 h-4" />
                {loading ? "Setting Up Session" : "New Chat"}
            </Button>
        {error ? (
                <p role="alert" className="text-sm text-red-600">
                {error}
                </p>
            ) : null
        }
        </div>
    );
}
