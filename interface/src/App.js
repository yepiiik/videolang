import logo from './logo.svg';
import './App.css';
import './index.css'
import SearchText from './api/SearchText';
import { useMemo, useState } from 'react';
import SearchForm from './components/forms/SearchForm';
import { useFetching } from './hooks/useFetching';
import VideoItem from './components/video/VideoItem';

function App() {
  const [responseData, setResponseData] = useState([])
  const [text, setText] = useState('')

  const [fetchText, isLoadingText, textError] = useFetching(async (text) => {
    setText(text)
    console.log(text)
    const response = await SearchText.findText(text);
    setResponseData(response.data)
  })


  return (
    <div className="App">
      <header className='main__header'>
        <SearchForm callback={fetchText}/>
      </header>
      <div className="container">
        {isLoadingText && 'loading...'}
        {text && <h3>{text}</h3>}
        <div className="wrapper">
          {responseData.map(video => 
            <VideoItem video={video} text={text}/>
          )}
        </div>        
      </div>
    </div>
  );
}

export default App;
