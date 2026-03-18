import React, { useState, useRef } from 'react';
import cl from './SearchForm.module.css';

const SearchForm = ({callback}) => {
    const [blockClasses, setBlockClasses] = useState([cl.search__form]);
    const [searchText, setSearchText] = useState('');

    const searchInput = useRef()

    const hideForm = () => {
        setBlockClasses([...blockClasses].filter(a => a !== cl.active))
        searchInput.current.blur()
    }

    const search = (e) => {
        e.preventDefault()
        hideForm()
        console.log(searchText)
        callback(searchText)
    }

    return (
        <form className={blockClasses.join(' ')} onSubmit={e => search(e)} onClick={() => hideForm()}>
            <div className={cl.search__block} onClick={e => e.stopPropagation()}>
                <input ref={searchInput} className={cl.search__input} type="text" placeholder='Search within captions...' onFocus={() => setBlockClasses([...blockClasses, cl.active])} onChange={(e) => setSearchText(e.target.value)} value={searchText}/>
                <button type='submit' className={cl.search__btn}>Search</button>
            </div>
        </form>
    );
}

export default SearchForm;
