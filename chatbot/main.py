from chatbot import build_graph
graph = build_graph()

while True:
    question = input("Ask a question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        break
    response = graph.invoke({"question": question})
    print("Answer:", response["answer"])