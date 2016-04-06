import 'aframe'
import 'babel-polyfill'
import {Animation, Entity, Scene} from 'aframe-react'
import React from 'react'
import { render } from 'react-dom'
import sample from 'lodash.sample'
import {cdn} from '../utils'
import {Camera, Cursor, Light, Sky, CurvedImage, VideoSphere} from '../components/primitives'
import {Sphere, Cube, Cylinder, Plane} from '../components/geometries'
import {
    SearchkitManager, SearchkitProvider,
    SearchBox, RefinementListFilter, MenuFilter,
    Hits, HitsStats, NoHits, Pagination, SortingSelector,
    SelectedFilters, ResetFilters, ItemHistogramList,
    Layout, LayoutBody, LayoutResults, TopBar,
    SideBar, ActionBar, ActionBarRow
} from "searchkit";

import { browserHistory, Router, Route, Link } from 'react-router'
require("./index.scss");
var ReactTHREE = require('react-three');
var THREE = require('three');
var Modal = require('react-modal');

const devhost = "http://192.168.99.100:9200/main_index"
const host = "https://d78cfb11f565e845000.qb0x.com/movies"
const sk = new SearchkitManager(devhost, {
  multipleSearchers:false
})



class ModelHits extends React.Component {
    render() {
     const result = this.props.result;
	let url = "https://s3.amazonaws.com/ncategorizer-assets/3d-models/" + result._location
	return (
	        <div className={bemBlocks.item().mix(bemBlocks.container("item"))} key={result._id}>
		  <a href={url} target="_blank">Download obj file.</a>
	          <img className={bemBlocks.item("thumbnail")} src={result._source.image_file} width="180" height="270"/>
		  <div className={bemBlocks.item("title")}>{result._source.title}</div>
		  <div className={bemBlocks.item("description")}>{result._source.description}</div>
		  <div className={bemBlocks.item("meta_data")}>{result._source.meta_data}</div>
		  <div className={bemBlocks.item("price")}>{result._source.price}</div>
		  <ModalViewer></ModalViewer>		
		</div>
	)
    }
}
var ModelRenderer = React.createClass({
    render: function() {
	var aspectratio = this.props.width / this.props.height;
	var cameraprops = {fov : 75, aspect : aspectratio,
			   near : 1, far : 5000,
			   position : new THREE.Vector3(0,0,600),
			   lookat : new THREE.Vector3(0,0,0)};

	return <Renderer width={this.props.width} height={this.props.height}>
	    <Scene width={this.props.width} height={this.props.height} camera="maincamera">
	    <PerspectiveCamera name="maincamera" {...cameraprops} />
	    <Cupcake {...this.props.cupcakedata} />
	    </Scene>
	    </Renderer>;
    }
});
var ModalViewer = React.createClass({

    getInitialState: function() {
	return { modalIsOpen: false };
    },

    openModal: function() {
	this.setState({modalIsOpen: true});
    },

    closeModal: function() {
	this.setState({modalIsOpen: false});
    },

    handleModalCloseRequest: function() {
	// opportunity to validate something and keep the modal open even if it
	// requested to be closed
	this.setState({modalIsOpen: false});
    },

    handleSaveClicked: function(e) {
	alert('Save button was clicked');
    },

    render: function() {
	return (
	    <div class="ModalViewer">
		    <button onClick={this.openModal}>Open Modal</button>
	             <Modal
	    className="Modal__Bootstrap modal-dialog"
	    closeTimeoutMS={150}
	    isOpen={this.state.modalIsOpen}
	    onRequestClose={this.handleModalCloseRequest}
	        >
		<div className="modal-content">
		<div className="modal-header">
		
		<button type="button" className="close" onClick={this.handleModalCloseRequest}>
		<span aria-hidden="true">&times;</span>
		<span className="sr-only">Close</span>
		</button>
		<h4 className="modal-title">Modal title</h4>
		</div>
		<div className="modal-body">
                <ModelRenderer></ModelRenderer>
	        </div>
	        </div>
	        </Modal>
	    </div>
	);
    }
});

export class DemoScene extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
  }


    render() {

	return (<div>

		<SearchkitProvider searchkit={sk}>
		  <div className="search">
		   <div className="search__query">
		    <SearchBox searchOnChange={true} prefixQueryFields={["actors^1","type^2","languages","title^10"]} />
		   </div>
		  <div className="search__results">
		   <Hits hitsPerPage={6} itemComponent={ModelHits}/>
		  </div>
		 </div>
		</SearchkitProvider>

		</div>);
    }
}
class App extends React.Component {
    render() {
	const depth = this.props.routes.length

	return (
	    <div>
	    <aside>
	    <ul>
	    <li><Link to={Products.path}>Products</Link></li>
	    <li><Link to={TextSearch.path}>Orders</Link></li>
	    </ul>
	    </aside>
	    <main>
	    <ul className="breadcrumbs-list">
	    {this.props.routes.map((item, index) =>
		<li key={index}>
		<Link
		onlyActiveOnIndex={true}
		activeClassName="breadcrumb-active"
		to={item.path || ''}>
		{item.component.title}
		</Link>
		{(index + 1) < depth && '\u2192'}
		</li>
	    )}
	    </ul>
	    {this.props.children}
	    </main>
	    </div>
	)
    }
}

App.title = 'Home'
App.path = '/search/home'



class Products extends React.Component {
    render() {
	return (
	    <div className="Page">
	    <h1>File Search</h1>
	    </div>
	)
    }
}

Products.title = 'File Search'
Products.path = '/search/upload'

class TextSearch extends React.Component {
    render() {
	return (
	    <div className="Page">
	    <h1>Search</h1>
	    <DemoScene/>
	    </div>
	)
    }
}

TextSearch.title = 'Search'
TextSearch.path = '/search'

render((
    <Router history={browserHistory}>
     <Route path={App.path} component={App}>
      <Route path={Products.path} component={Products} />
      <Route path={TextSearch.path} component={TextSearch} />
     </Route>
    </Router>
), document.getElementById('react-app'))

//ReactDOM.render(<DemoScene/>, document.querySelector('.scene-container'))

