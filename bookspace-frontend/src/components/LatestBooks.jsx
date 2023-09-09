import { useEffect, useState } from 'react'

const LatestBooks = () => {
  const [books, setBooks] = useState([])
  const [authors, setAuthors] = useState([])

  useEffect(() => {
    // Fetch data from API endPoints
    fetch('http://127.0.0.1:8000/main/books/')
      .then((response) => response.json())
      .then((bookData) => {
        // update state from fetched book data
        setBooks(bookData)
      })

    // Fetch author data from the  `authors` endpoint
    fetch('http://127.0.0.1:8000/main/authors/')
      .then((response) => response.json)
      .then((authorData) => {
        // look up object to match author id to the book
        const authorLookup = {}
        authorData.forEach((author) => {
          authorLookup[author.id] = author.name
        })

        // update state using fetched author data
        setAuthors(authorLookup)
      })
      .catch((error) => {
        console.error('Error fetching author data:', error)
      })
  }, [])

  return (
    <div>
      {books.map((book, index) => (
        <div className="flex mb-4" key={index}>
          <div className="m-2">
            {/* Using thumbnail url from book-images API */}
            <img src={book.thumbnail} alt={`book ${book.index}`} />
          </div>
          <div className="ml-8 mt-4">
            <h2 className="text-xl font-bold text-blue-800">{book.title}</h2>
            <p>
              <span className="text-gray-500">{authors[book.author_id]}</span>
            </p>
            <p className="text-gray-800">
              {`Publication Date: ${book.publication_date}`}
            </p>
            <p>{`Book Tags: ${book.tag}`}</p>
          </div>
        </div>
      ))}

      {/* <div className="flex mb-4">
        <div className="m-2">
          <img
            src="https://www.publishersweekly.com/cover/9780671666255"
            alt="book 1"
            className="h-24 w-[96px]"
          />
        </div>
        <div className="ml-8 mt-4">
          <h2 className="text-xl font-bold text-blue-800">American Star</h2>
          <p>
            <span className="text-gray-500">
              William S. Walsh (1854 - 1919)
            </span>
          </p>
          <p className="text-gray-800">Complete | Collaborative | English</p>
        </div>
      </div> */}
    </div>
  )
}

export default LatestBooks
