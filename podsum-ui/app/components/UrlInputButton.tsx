'use client';

import React, { useState } from 'react';

interface Props {
    // Add any props you need
}

interface Segment {
    segment_title: string;
    description: string;
    direct_quote: string;
    timestamp: string;
}

const UrlInputButton: React.FC<Props> = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [status, setStatus] = useState('');
    const [summary, setSummary] = useState<Segment[]>([]);

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setLoading(true);
        setSummary([]);

        try {
            setStatus('Transcribing podcast...');
            const transcribeResponse = await fetch('http://localhost:8000/transcribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url }),
            });
            const transcribeData = await transcribeResponse.json();

            setStatus('Summarizing podcast...');
            const summarizeResponse = await fetch('http://localhost:8000/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: transcribeData.id }),
            });
            const summarizeData = await summarizeResponse.json();

            setSummary(summarizeData);
            setStatus('Summary complete!');
        } catch (error) {
            console.error(error);
            setStatus('An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center">
            <form onSubmit={handleSubmit} className="w-full max-w-md mb-4">
                <input
                    type="text"
                    value={url}
                    onChange={(event) => setUrl(event.target.value)}
                    placeholder="Enter podcast URL"
                    className="w-full p-2 mb-2 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg disabled:opacity-50"
                >
                    {loading ? 'Processing...' : 'Submit'}
                </button>
            </form>
            {status && <p className="mb-4 text-center">{status}</p>}
            {summary.length > 0 && (
                <div className="w-full max-w-2xl">
                    <h2 className="text-2xl font-bold mb-4">Podcast Chapters</h2>
                    {summary.map((segment, index) => (
                        <div key={index} className="mb-6 p-4 bg-gray-100 rounded-lg">
                            <h3 className="text-xl font-semibold mb-2">Chapter {index + 1}: {segment.segment_title}</h3>
                            <p className="mb-2"><strong>Description:</strong> {segment.description}</p>
                            <p className="mb-2"><strong>Highlight Quote:</strong> "{segment.direct_quote}"</p>
                            <p><strong>Timestamp:</strong> {segment.timestamp}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default UrlInputButton;