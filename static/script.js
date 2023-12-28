const input = document.querySelector(".input")
const output = document.querySelector(".output")
const add = document.querySelector(".add")

add.addEventListener("click", async () => {
    const word = input.value
    input.value = ""
    const response = await fetch("http://127.0.0.1:8000/word?word=" + word)
    const result = await response.json()
    output.value = output.value + result["result"]

})