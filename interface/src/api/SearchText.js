import axios from "axios";

export default class SearchText {
    static async findText(text) {
        const response = await axios.get("http://127.0.0.1:5000/fast_find_text", {
            params: {
                q: text
            }
        })
        
        return response
    }
}