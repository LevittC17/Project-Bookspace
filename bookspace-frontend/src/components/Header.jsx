import { useEffect, useState } from 'react'
import logoiconImage from '../assets/logoicon.png'

const Header = () => {
  const [input, setInput] = useState('')
  const [searchResults, setSearchResults] = useState([])

  const fetchSearchResults = async () => {
    try {
      if (input.trim() !== '') {
        const response = await fetch(
          `http://127.0.0.1:8000/main/books/?search=${input}`
        )
        if (response.ok) {
          const data = await response.json()
          setSearchResults(data)
        } else {
          console.log('Failed to fetch search results')
        }
      } else {
        setSearchResults([]) // clear results if empty input
      }
    } catch (error) {
      console.error('Error fetching results', error)
    }
  }

  useEffect(() => {
    fetchSearchResults()
  }, [input])

  const handleChange = (e) => {
    setInput(e.target.value)
  }

  return (
    <div className="flex flex-col sm:flex-row mt-[80px]">
      {/* Left Div: Header */}
      <div className="flex flex-wrap text-blue-800 w-full sm:w-4/5">
        <img src={logoiconImage} alt="Bookspace Logo" className="logo" />
        <h1 className="text-2xl sm:text-4xl">BOOKSPACE</h1>
      </div>

      <div className="flex sm:flex-wrap">
        <div className=" flex w-full h-10 pl-0 sm:w-1/4">
          <input
            type="text"
            className="w-64 text-black p-2 rounded border border-blue-800 focus:border-blue-800"
            placeholder="Search..."
            value={input}
            onChange={handleChange}
          />
          <button
            className="bg-blue-800 text-white px-4 py-2 ml-2 rounded hover:bg-white hover:text-blue-800 transition"
            onClick={fetchSearchResults}
          >
            Search
          </button>
        </div>

        {/* Display Search Results if input !== [] */}

        {searchResults.length > 0 && (
          <div className="text-blue-800">
            <h2 className="text-xl font-bold">Search Results</h2>
            <hr className="border-[1px] border-blue-800" />
            <ul>
              {searchResults.map((book) => (
                <li key={book.id}>
                  <h3 className="text-lg">{book.name}</h3>
                  <p>
                    <span>&rarr;</span>
                    {book.description}
                  </p>
                  <p>
                    Publication Date:{' '}
                    <span className="text-cyan-600">
                      {book.publication_date}
                    </span>
                  </p>
                  <p>
                    Price: <span className="text-cyan-600">{book.price}</span>
                  </p>
                  <hr className="border-[1px] border-blue-800 mb-4" />
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default Header
