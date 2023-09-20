<template>
	<view class="row">
		<uv-toast ref='toast'></uv-toast>
		<view class="status_bar" style="height: var(--status-bar-height); width: 100%;">
		</view>
		<view class="Search">
			<view class='info_box'>
				<uv-button icon='email-fill' color="white" iconColor="#FF5A5F" class='message_button' size='large'
					@click="toAlert"></uv-button>
				<uv-badge type="error" max="99" :value="info_num" class='info_num' :offset="[100,100]"></uv-badge>
			</view>
			<uv-search v-model='con' @search="toSearch" @custom="toSearch" bgColor="white" border-color="#FF5A5F"
				color="#FF5A5F" placeholderColor="#FFC0CB" searchIconColor="#FF5A5F"></uv-search>
		</view>
		<uv-tabs :list="tab_list" @change='changeTab' :activeStyle="{
					color: '#FF5A5F',
					fontWeight: 'bold',
					transform: 'scale(1.05)'
		    	}" lineColor='#FF5A5F'></uv-tabs>
		<view style="height: 5rpx;"></view>
		<uv-tabs :list="order_list" @change='changeOrder' :activeStyle="{
					color: '#FF5A5F',
					fontWeight: 'bold',
					fontSize: '30rpx'
		    	}" :inactiveStyle="{
					fontSize:'30rpx'
				}" :itemStyle="{
					height:'35rpx',
				}" lineColor='transparent'></uv-tabs>
		<uv-loading-icon mode="circle" color="#FF5A5F" size='40' :show='load_state'></uv-loading-icon>
		<view v-if='Page.rule == "time"' style='background-color: #f1f1f1;'>
			<uv-swiper :list="list" circular class='swBox' height="180" keyName="image" showTitle @click="swiper_Show"
				v-if='show_time'></uv-swiper>
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
			<uv-load-more :status="loadAble" v-if='show_time'></uv-load-more>
		</view>
		<view v-if='Page.rule=="like"' style="margin-top: 20rpx;">
			<view v-for='(img,index) in PrevList' :key='img.iid'>
				<view class='like_card' @click="toShow(img.iid)">
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
				iid: '',
				info_num: '',
				uid: '',
				load_state:true,
				first:true
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
			toAlert() {
				if(this.uid=='')
				{
					this.$refs.toast.show({
						message:'请先登录',
						type:'error',
						position:'top'
					})
					return
				}
				uni.navigateTo({
					url: '/pages/Alert/Alert'
				})
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
						"tag": this.Page.tag
					}
				} else if (this.Page.page == 1) {
					form = {
						"page": 1,
						"per_page": this.Page.per_page,
						"rule": "time",
						"tag": this.Page.tag
					}
				} else {
					form = {
						"page": this.Page.page,
						"per_page": this.Page.per_page,
						"rule": "time",
						"iid": this.iid,
						"tag": this.Page.tag
					}
				}
				uni.request({
					url: "http://8.137.96.56:3689/img/select_tag",
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
					} else
						_this.PrevList = resp.data.prev_imgs
				}).catch(e=>{
					_this.$refs.toast.show({
						message:'服务器出错',
						icon:'error',
						position:'top'
					})
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
				if (this.uid != '') form['uid'] = this.uid

				uni.request({
					url: "http://8.137.96.56:3689/img/select",
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
					_this.info_num = resp.data.info_num

				}).catch(e=>{
					_this.$refs.toast.show({
						message:'服务器出错',
						icon:'error',
						position:'top'
					})
				})
			},
			swiper_Show(index) {
				const iid = this.list[index].iid
				this.toShow(iid)
			},
			toShow(iid) {
				if(this.uid=='')
				{
					this.$refs.toast.show({
						message:'登录后可见详情',
						type:'error',
						position:'top'
					})
					return
				}
				uni.navigateTo({
					url: '/pages/showImg/showImg?iid=' + iid
				})
			},
			toSearch() {
				if (this.con == '') {
					_this.$refs.toast.show({
						message:'请输入关键字',
						icon:'error',
						position:'top'
					})
					return false
				}
				uni.navigateTo({
					url: '/pages/search/search?con=' + this.con
				})
			}
		},
		mounted() {
			if(uni.getStorageSync('u_info'))
				this.uid = uni.getStorageSync('u_info').uid
			else this.uid=''
			this.imgSelect()
			this.load_state = false
			this.first = false
		},
		onShow(){
			if(this.first)return
			let _this = this
			uni.request({
				url:'http://8.137.96.56:3689/alert/get_num',
				method:'POST',
				data:_this.uid
			}).then(function(resp){
				_this.info_num = resp.data
			})
		},
		onReachBottom() {
			if (this.Page.rule == 'like') return;
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
			margin-top: 10rpx;
			padding-top: 20rpx;
			// border: solid #FF5A5F 1rpx;
		}

		.ImgsBox {
			display: flex;
		}

		.Search {
			padding-top: 20rpx;
			padding-left: 10rpx;
			display: flex;

			.info_box {
				display: flex;
				width: 80rpx;

				.message_button {
					width: 80rpx;
				}

				.info_num {
					height: 30rpx;
					position: relative;
					right: 30rpx;
					top: 5rpx;
				}
			}
		}

		.like_card {
			width: 750rpx;
			height: 300rpx;
			display: flex;

			.order {
				width: 50rpx;
				height: auto;
				color: white;
				text-align: center;
				vertical-align: middle;
				font-size: 40rpx;
				padding-top: 130rpx;
				font-weight: bold;
				background-color: #FF5A5F;
			}

			.image {
				margin-top: 25rpx;
				margin-left: 10rpx;
				width: 250rpx;
				height: 250rpx;
			}

			.text_info {
				width: 405rpx;
				height: auto;
				margin-left: 20rpx;
				padding-top: 20rpx;
				padding-bottom: 20rpx;
				display: block;

				.title {
					font-size: 40rpx;
					font-weight: bold;
				}

				.tag {
					font-size: 30rpx;
					color: #F4A7B9;
					margin-top: 20rpx;
				}

				.writer {
					color: #F4A7B9;
					margin-top: 20rpx;
				}

				.like {
					margin-top: 40rpx;
					color: #E63946;
				}
			}
		}
	}
</style>