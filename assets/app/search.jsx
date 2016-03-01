import 'aframe-core';

import 'babel-polyfill';

import {Animation, Entity, Scene} from 'aframe-react';


import * as React from "react";

import {
	SearchkitManager,
	SearchkitProvider,
	SearchBox,
	Hits
} from "searchkit";

require("./index.scss");

const host = "https://d78cfb11f565e845000.qb0x.com/movies"
const sk = new SearchkitManager(host, {
  multipleSearchers:false
})

class MovieHits extends Hits {
	renderResult(result) {
		let url = "http://www.imdb.com/title/" + result._source.imdbId
		return (
			<div className={this.bemBlocks.item().mix(this.bemBlocks.container("item"))} key={result._id}>
				<a href={url} target="_blank">
					<img className={this.bemBlocks.item("poster")} src={result._source.poster} width="180" height="270"/>
					<div className={this.bemBlocks.item("title")}>{result._source.title}</div>
				</a>
			</div>
		)
	}
}
class ModelHits extends Hits {
    renderResult(result) {
	let urlobj = "http://www.imdb.com/title/" + result._source.imdbId
	return (
	    <div className={this.bemBlocks.item().mix(this.bemBlocks.container("item"))} key={result._id}>
		<a href={url} target="_blank">
		     <a-model src="https://aframe.io/aframe/examples/_models/tree1/tree1.dae"></a-model>
		    
		    <div className={this.bemBlocks.item("title")}>{result._source.title}</div>
		</a>
	    </div>
	)
    }
}

export default class App extends React.Component {
	render() {
		return (
		<div className="search-site">
			<SearchkitProvider searchkit={sk}>
				<div>
					<div className="search-site__query">
						<SearchBox autofocus={true} searchOnChange={true} queryFields={["tags^1"]}/>
					</div>

					<div className="search-site__results">
						<ModelHits hitsPerPage={10}/>
					</div>
				</div>
			</SearchkitProvider>
		</div>

		);
	}
}
