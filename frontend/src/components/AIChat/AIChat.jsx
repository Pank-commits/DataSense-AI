import { useState } from "react";
import { FaRobot, FaPaperPlane, FaDatabase, FaExternalLinkAlt } from "react-icons/fa";
import { Link } from "react-router-dom";
import { askDataSenseAI } from "../../Services/aiServices";

function AIChat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) return;

    // Add user message
    setMessages((previous) => [
      ...previous,
      {
        type: "user",
        text: trimmedQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const data = await askDataSenseAI(trimmedQuestion);

      // Add AI response
      setMessages((previous) => [
        ...previous,
        {
          type: "assistant",
          text: data.answer,
          datasets: data.datasets || [],
        },
      ]);
    } catch (error) {
      console.error("AI request failed:", error);

      setMessages((previous) => [
        ...previous,
        {
          type: "error",
          text: "Sorry, I couldn't process your request. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto w-full max-w-5xl">
      {/* Header */}
      <div className="mb-6 flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-500 text-white shadow-lg">
          <FaRobot size={22} />
        </div>

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            DataSense AI
          </h1>

          <p className="text-slate-500">
            Ask me to find the right dataset for your project.
          </p>
        </div>
      </div>

      {/* Chat Box */}
      <div className="flex min-h-[550px] flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl">
        {/* Messages */}
        <div className="flex-1 space-y-5 overflow-y-auto p-6">
          {messages.length === 0 && (
            <div className="flex min-h-[400px] flex-col items-center justify-center text-center">
              <div className="mb-5 flex h-20 w-20 items-center justify-center rounded-full bg-cyan-50 text-cyan-500">
                <FaRobot size={36} />
              </div>

              <h2 className="text-2xl font-bold text-slate-800">
                How can I help?
              </h2>

              <p className="mt-2 max-w-lg text-slate-500">
                Ask me about datasets, machine learning tasks,
                categories, or dataset recommendations.
              </p>

              <div className="mt-6 flex flex-wrap justify-center gap-3">
                <button
                  type="button"
                  onClick={() =>
                    setQuestion(
                      "Recommend a healthcare dataset for predicting heart disease."
                    )
                  }
                  className="rounded-full border border-slate-200 px-4 py-2 text-sm text-slate-600 transition hover:border-cyan-400 hover:text-cyan-600"
                >
                  Healthcare dataset
                </button>

                <button
                  type="button"
                  onClick={() =>
                    setQuestion(
                      "Which datasets are suitable for classification?"
                    )
                  }
                  className="rounded-full border border-slate-200 px-4 py-2 text-sm text-slate-600 transition hover:border-cyan-400 hover:text-cyan-600"
                >
                  Classification datasets
                </button>

                <button
                  type="button"
                  onClick={() =>
                    setQuestion(
                      "Recommend a dataset for a beginner machine learning project."
                    )
                  }
                  className="rounded-full border border-slate-200 px-4 py-2 text-sm text-slate-600 transition hover:border-cyan-400 hover:text-cyan-600"
                >
                  Beginner dataset
                </button>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={index}>
              {/* User */}
              {message.type === "user" && (
                <div className="flex justify-end">
                  <div className="max-w-[80%] rounded-2xl rounded-br-md bg-blue-600 px-5 py-3 text-white shadow-sm">
                    {message.text}
                  </div>
                </div>
              )}

              {/* Assistant */}
              {message.type === "assistant" && (
                <div className="flex items-start gap-3">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-cyan-500 text-white">
                    <FaRobot size={16} />
                  </div>

                  <div className="max-w-[85%]">
                    <div className="whitespace-pre-line rounded-2xl rounded-tl-md bg-slate-100 px-5 py-4 text-slate-700">
                      {message.text}
                    </div>

                    {/* Recommended datasets */}
                    {message.datasets.length > 0 && (
                      <div className="mt-4 space-y-3">
                        <p className="text-sm font-semibold text-slate-600">
                          Recommended datasets
                        </p>

                        {message.datasets.map((dataset) => (
                          <Link
                            key={dataset.id}
                            to={`/datasets/${dataset.slug}`}
                            className="block rounded-xl border border-slate-200 bg-white p-4 shadow-sm transition hover:-translate-y-0.5 hover:border-cyan-300 hover:shadow-md"
                          >
                            <div className="flex items-start justify-between gap-4">
                              <div className="flex items-start gap-3">
                                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-cyan-50 text-cyan-600">
                                  <FaDatabase />
                                </div>

                                <div>
                                  <h3 className="font-semibold text-slate-800">
                                    {dataset.name}
                                  </h3>

                                  <div className="mt-1 flex flex-wrap gap-2 text-xs">
                                    <span className="rounded-full bg-blue-50 px-2 py-1 text-blue-600">
                                      {dataset.category}
                                    </span>

                                    <span className="rounded-full bg-purple-50 px-2 py-1 text-purple-600">
                                      {dataset.ml_task}
                                    </span>
                                  </div>
                                </div>
                              </div>

                              <FaExternalLinkAlt className="mt-1 text-slate-400" size={14} />
                            </div>
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Error */}
              {message.type === "error" && (
                <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-600">
                  {message.text}
                </div>
              )}
            </div>
          ))}

          {/* Loading */}
          {loading && (
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-cyan-500 text-white">
                <FaRobot size={16} />
              </div>

              <div className="rounded-2xl rounded-tl-md bg-slate-100 px-5 py-4 text-slate-500">
                <span className="animate-pulse">
                  DataSense AI is thinking...
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <form
          onSubmit={handleSubmit}
          className="border-t border-slate-200 bg-slate-50 p-4"
        >
          <div className="flex items-center gap-3">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask DataSense AI..."
              disabled={loading}
              className="flex-1 rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-100 disabled:bg-slate-100"
            />

            <button
              type="submit"
              disabled={!question.trim() || loading}
              className="flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-500 text-white transition hover:bg-cyan-600 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <FaPaperPlane />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AIChat;
