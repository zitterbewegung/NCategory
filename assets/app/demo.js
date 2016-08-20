import 'aframe-core'
import 'babel-polyfill'
import {Animation, Entity, Scene} from 'aframe-react'
import React from 'react'
import ReactDOM from 'react-dom'
import sample from 'lodash.sample'
import {cdn} from '../utils'
import {Camera, Cursor, Light, Sky, CurvedImage, VideoSphere} from '../components/primitives'
import {Sphere, Cube, Cylinder, Plane} from '../components/geometries'
import {
    SearchBox,
    RefinementListFilter,
    Hits,
    HitsStats,
    HitItemProps,
    SearchkitComponent,
    SelectedFilters,
    MenuFilter,
    HierarchicalMenuFilter,
    Pagination,
    ResetFilters,
    SearchkitManager,
    SearchkitProvider,
    NoHits
} from "searchkit";
require("./index.scss");
var ReactTHREE = require('react-three');
var THREE = require('three');
var Modal = require('react-modal');
var ReactS3Uploader = require('react-s3-uploader');
const ip = "192.168.99.100"
const devhost = "http://192.168.99.100:9200/main_index"
const host = "https://d78cfb11f565e845000.qb0x.com/movies"
const sk = new SearchkitManager(devhost, {
  multipleSearchers:false
})

const ModelHits = (props) => {


	let url = "https://s3.amazonaws.com/ncategorizer-assets/3d-models/" + props.result._source.image_file;
    return(
      	<div className={props.bemBlocks.item().mix(props.bemBlocks.container("item"))} key={props.result._id}>
		<a href={url} target="_blank">
		
	        <img className={props.bemBlocks.item("thumbnail")} src={props.result._source.image_file} width="180" height="270"/>
		<div className={props.bemBlocks.item("title")}>{props.result._source.title}</div>
			<div className={props.bemBlocks.item("description")}>{props.result._source.description}</div>
		
		<div className={props.bemBlocks.item("price")}>Available ${props.result._source.price}</div>
		
		</a>
	    </div>
    );
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

class DemoScene extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
  }

  render () {



      return (
	  <div>
	  
	  <SearchkitProvider searchkit={sk}>
	      <div className="search">
		  <div className="search__query">
		
	              <SearchBox searchOnChange={true}/>
		             <ReactS3Uploader
				 signingUrl="/s3/sign"
				 accept="application/sla"
				 preprocess={this.onUploadStart}
				 onProgress={this.onUploadProgress}
				 onError={this.onUploadError}
				 onFinish={this.onUploadFinish}
				 uploadRequestHeaders={{ 'x-amz-acl': 'public-read' }}
				 contentDisposition="auto"
				 server="http://192.168.99.100" />
			     
	 	  </div>
		  <div className="search__results">
		      <Hits hitsPerPage={6} mod="sk-hits-grid" itemComponent={ModelHits}/>
		      <NoHits translations={{
			  "NoHits.NoResultsFound":"No movies found were found for {query}",
			  "NoHits.DidYouMean":"Search for {suggestion}",
			  "NoHits.SearchWithoutFilters":"Search for {query} without filters"
		      }} suggestionsField="title"/>
		      <Pagination showNumbers={true}/>
		  </div>
	      </div>
	  </SearchkitProvider>

	  </div>);
         }
   
}


ReactDOM.render(<DemoScene/>, document.querySelector('.scene-container'))

