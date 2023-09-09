import React from 'react'

const NewsSection = () => {
  return (
    <div>
      {/* {news.map((item, index) => (
            // news content goes here
        ))} */}
      <div className="mb-4">
        <h1 className="text-2xl font-bold">
          <a href="" className="text-blue-800">
            18 Years and Counting
          </a>
        </h1>
        <p className="text-gray-500">Posted on September 23 2023</p>
        <p className="text-gray-800">
          {/* {item.content.length > 100
            ? `${item.content.substring(0, 100)}[...]`
            : item.content} */}
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Harum,
          numquam ab soluta atque suscipit itaque, illo vitae saepe odio sequi
          fuga beatae! Aut sequi tenetur, ducimus voluptatem numquam voluptate
          tempora!
        </p>
      </div>

      <div className="mb-4">
        <h1 className="text-2xl font-bold">
          <a href="" className="text-blue-800">
            18 Years and Counting
          </a>
        </h1>
        <p className="text-gray-500">Posted on September 23 2023</p>
        <p className="text-gray-800">
          {/* {item.content.length > 100
            ? `${item.content.substring(0, 100)}[...]`
            : item.content} */}
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Harum,
          numquam ab soluta atque suscipit itaque, illo vitae saepe odio sequi
          fuga beatae! Aut sequi tenetur, ducimus voluptatem numquam voluptate
          tempora!
        </p>
      </div>
    </div>
  )
}

export default NewsSection
