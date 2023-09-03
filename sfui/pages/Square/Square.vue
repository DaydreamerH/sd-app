<template>
	<view class="row">
		<view class="Search">
			<uv-search v-model='con' @search="toSearch" @custom="toSearch" bgColor="#D2E8E8" border-color="#2A9D8F"
				color="#2A9D8F" placeholderColor="#8AC0C0" searchIconColor="#8AC0C0"></uv-search>
		</view>
		<uv-tabs :list="tab_list" @change='changeTab' :activeStyle="{
					color: '#2A9D8F',
					fontWeight: 'bold',
					transform: 'scale(1.05)'
		    	}" lineColor='#2A9D8F'></uv-tabs>
		<view style="height: 5rpx;"></view>
		<uv-tabs :list="order_list" @change='changeOrder' :activeStyle="{
					color: '#2A9D8F',
					fontWeight: 'bold',
					fontSize: '30rpx'
		    	}" :inactiveStyle="{
					fontSize:'30rpx'
				}" :itemStyle="{
					height:'35rpx'
				}" lineColor='transparent'></uv-tabs>
		<view v-if='Page.rule == "time"'>
			<uv-swiper :list="list" circular class='swBox' height="180" keyName="image" showTitle @click="swiper_Show"
				bgColor="#D2E8E8"></uv-swiper>
			<view v-for='(imgs,index) in pairedPrevImgs' :key='index' class="ImgsBox">
				<view v-for='(img,index) in imgs' :key='img.iid'>
					<view v-if='show_time&&index==0' @click="toShow(img.iid)">
						<ImgCard v-if='show_time&&index==0' :img_url='img.source' :title='img.title'></ImgCard>
					</view>
					<view v-if='show_time&&index==1' @click="toShow(img.iid)">
						<ImgCardRight v-if='show_time&&index==1' :img_url='img.source' :title='img.title'>
						</ImgCardRight>
					</view>
				</view>
			</view>
			<uv-load-more :status="loadAble"></uv-load-more>
		</view>
		<view v-if='Page.rule=="like"' style="margin-top: 20rpx;">
			<view v-for='(img,index) in PrevList' :key='img.iid'>
				<view class='like_card'  @click="toShow(img.iid)">
					<view class='order'>
						{{index+1}}
					</view>
					<image :src='img.source' class='image'></image>
					<view class='text_info'>
						<view class='title'>
							{{img.title}}
						</view>
						<view class='tag'>
							{{img.tag}}
						</view>
						<view class='writer'>
							{{img.uname}}
						</view>
						<view class='like'>
							被收藏次数：{{img.like_num}}
						</view>
					</view>
				</view>
				<uv-line></uv-line>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				PrevList: [],
				Page: {
					page: 1,
					per_page: 4,
					tag: "",
					rule: 'time'
				},
				total_pages: '',
				show_time: false,
				loadAble: "loadmore",
				list: [

				],
				tab_list: [{
					name: '总览'
				}, {
					name: '动漫卡通'
				}, {
					name: '建筑艺术',
				}, {
					name: '写实人像'
				}, {
					name: '欧美漫画'
				}],
				current: 0,
				con: '',
				order_list: [{
					name: '最新'
				}, {
					name: '热门'
				}],
				iid: ''
			}
		},
		methods: {
			changeTab(item) {
				this.current = item.index
				this.Page.page = 1
				if (this.current == 0)
					this.imgSelect()
				else this.imgSelectTag()
			},
			changeOrder(item) {
				this.Page.page = 1
				if (item.index == 0)
					this.Page.rule = 'time'
				else
					this.Page.rule = 'like'
				if (this.current == 0)
					this.imgSelect()
				else 
					this.imgSelectTag()
			},
			imgSelectTag() {
				let _this = this
				let form = {}
				this.Page.tag = this.tab_list[this.current].name
				if (this.Page.rule == 'like') {
					form = {
						"rule": "like",
						"tag":this.Page.tag
					}
				} else if (this.Page.page == 1) {
					form = {
						"page": 1,
						"per_page": this.Page.per_page,
						"rule": "time",
						"tag":this.Page.tag
					}
				} else {
					form = {
						"page": this.Page.page,
						"per_page": this.Page.per_page,
						"rule": "time",
						"iid": this.iid,
						"tag":this.Page.tag
					}
				}
				uni.request({
					url: "http://localhost:3689/img/select_tag",
					data: form,
					method: 'POST'
				}).then(function(resp) {
					if (_this.Page.rule == 'time') {
						if (_this.Page.page == 1) {
							_this.PrevList = resp.data.prev_imgs
							_this.list = resp.data.hot_imgs
							_this.show_time = true
							_this.iid = resp.data.iid
						} else _this.PrevList = _this.PrevList.concat(resp.data.prev_imgs)
						_this.total_pages = resp.data.total_pages
					}
					else 
						_this.PrevList = resp.data.prev_imgs
				})
			},
			imgSelect() {
				let _this = this
				let form = {}
				if (this.Page.rule == 'like') {
					form = {
						"rule": "like"
					}
				} else if (this.Page.page == 1) {
					form = {
						"page": 1,
						"per_page": this.Page.per_page,
						"rule": "time"
					}
				} else {
					form = {
						"page": this.Page.page,
						"per_page": this.Page.per_page,
						"rule": "time",
						"iid": this.iid
					}
				}
				uni.request({
					url: "http://localhost:3689/img/select",
					method: 'POST',
					data: form
				}).then(function(resp) {
					if (_this.Page.rule == 'time') {
						if (_this.Page.page == 1) {
							_this.PrevList = resp.data.prev_imgs
							_this.list = resp.data.hot_imgs
							_this.show_time = true
							_this.iid = resp.data.iid
						} else _this.PrevList = _this.PrevList.concat(resp.data.prev_imgs)
						_this.total_pages = resp.data.total_pages
					} else _this.PrevList = resp.data.prev_imgs
				})
			},
			swiper_Show(index) {
				const iid = this.list[index].iid
				this.toShow(iid)
			},
			toShow(iid) {
				uni.navigateTo({
					url: '/pages/showImg/showImg?iid=' + iid
				})
			},
			toSearch() {
				if(this.con==''){
					uni.showToast({
						title:"请输入关键字喵",
						icon:"error"
					})
					return false
				}
				uni.navigateTo({
					url: '/pages/search/search?con=' + this.con
				})
			}
		},
		mounted() {
			this.imgSelect()
		},
		onReachBottom() {
			if(this.Page.rule=='like')return;
			let _this = this
			this.Page.page += 1
			this.loadAble = 'loading'
			if (this.total_pages >= this.Page.page) {
				if (this.current == 0)
					this.imgSelect()
				else this.imgSelectTag()
				this.loadAble = 'loadmore'
			} else this.loadAble = 'nomore'
		},
		onPullDownRefresh() {
			let _this = this
			this.show_time = false
			this.Page.page = 1
			if (this.current == 0) this.imgSelect()
			else this.imgSelectTag()

			uni.stopPullDownRefresh()
		},
		computed: {
			isLeft(index) {
				if (index % 2 != 0) return false
				return true
			},
			pairedPrevImgs() {
				const pairedPrevImgs = [];
				for (let i = 0; i < this.PrevList.length; i += 2) {
					const pair = this.PrevList.slice(i, i + 2);
					pairedPrevImgs.push(pair);
				}
				return pairedPrevImgs;
			}
		}
	}
</script>

<style lang="scss" scoped>
	.row {
		width: 750rpx;
		min-height: 100vh;
		background-color: white;
		height: auto;

		.line {
			position: relative;
			top: -5rpx;
		}

		.swBox {
			width: 710rpx;
			margin-left: 20rpx;
			margin-top: 20rpx;
			border: solid #2A9D8F 1rpx;
		}

		.ImgsBox {
			display: flex;
		}

		.Search {
			padding-top: 20rpx;
			margin-bottom: 10rpx;
			padding-left: 10rpx;
		}
		
		.like_card{
			width:750rpx;
			height:300rpx;
			display: flex;
			.order{
				width:50rpx;
				height:auto;
				color: white;
				text-align: center;
				vertical-align: middle;
				font-size: 40rpx;
				padding-top: 130rpx;
				font-weight: bold;
				background-color: #2A9D8F;
			}
			.image{
				margin-top: 25rpx;
				margin-left: 10rpx;
				width: 250rpx;
				height: 250rpx;
			}
			.text_info{
				width: 405rpx;
				height: auto;
				margin-left: 20rpx;
				padding-top: 20rpx;
				padding-bottom: 20rpx;
				display: block;
				.title{
					font-size:40rpx;
					font-weight: bold;
				}
				.tag{
					font-size: 30rpx;
					color: #8AC0C0;
					margin-top: 20rpx;
				}
				.writer{
					color: #2A9D8F;
					margin-top: 20rpx;
				}
				.like{
					margin-top: 40rpx;
					color: #E63946;
				}
			}
		}
	}
</style>