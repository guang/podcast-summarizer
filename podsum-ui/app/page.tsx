import UrlInputButton from "./components/UrlInputButton";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Guang's Awesome Podcast Summarizer</h1>
        <p className="text-xl text-gray-600 mb-8">Easily summarize your favorite podcasts</p>
      </div>

      <div className="bg-white p-8 rounded-lg shadow-md">
        <UrlInputButton />
      </div>
    </main>
  );
}
