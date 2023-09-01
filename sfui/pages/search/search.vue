<template>
	<view class="row">
		<view class="Search">
			<uv-search v-model='con' @search="Search" @custom="Search" bgColor="#D2E8E8" border-color="#2A9D8F"
				color="#2A9D8F" placeholderColor="#8AC0C0" searchIconColor="#8AC0C0"></uv-search>
		</view>
		<view v-for='(imgs,index) in pairedPrevImgs' :key='index' class="ImgsBox">
			<view v-for='(img,index) in imgs' :key='img.iid'>
				<view v-if='show_time&&index==0' @click="toShow(img.iid)">
					<ImgCard v-if='show_time&&index==0' :img_url='img.source' :title='img.title'></ImgCard>
				</view>
				<view v-if='show_time&&index==1' @click="toShow(img.iid)">
					<ImgCardRight v-if='show_time&&index==1' :img_url='img.source' :title='img.title'></ImgCardRight>
				</view>
			</view>
		</view>
		<uv-load-more :status="loadAble"></uv-load-more>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				result: [],
				page: 1,
				per_page: 6,
				total_pages: '',
				show_time: false,
				con: '',
				loadAble: 'loadmore',
				iid: ''
			};
		},
		methods: {
			getImg() {
				let form = {}
				if (this.page == 1) {
					form = {
						page: this.page,
						per_page: this.per_page,
						con: this.con
					}
					this.show_time = false
				} else {
					form = {
						page: this.page,
						per_page: this.per_page,
						con: this.con,
						iid: this.iid
					}
				}
				let _this = this
				uni.request({
					data: form,
					method: "POST",
					url: 'http://localhost:3689/img/select_con'
				}).then(function(resp) {
					if (_this.page == 1) {
						_this.result = resp.data.img_list
						_this.show_time = true
						_this.iid = resp.data.max_iid
					} else _this.result = _this.result.concat(resp.data.img_list)
					_this.total_pages = resp.data.total_pages
				})
			},
			toShow(iid) {
				uni.navigateTo({
					url: '/pages/showImg/showImg?iid=' + iid
				})
			},
			Search() {
				this.page = 1
				this.getImg()
			}
		},
		onLoad(option) {
			this.con = option.con
			const form = {
				page: this.page,
				per_page: this.per_page,
				con: this.con
			}
			let _this = this
			uni.request({
				url: 'http://localhost:3689/img/select_con',
				method: 'POST',
				data: form
			}).then(function(resp) {
				_this.result = resp.data.img_list
				_this.total_pages = resp.data.total_pages
				_this.show_time = true
				_this.iid = resp.data.max_iid
			})
		},
		computed: {
			pairedPrevImgs() {
				const pairedPrevImgs = []
				for (let i = 0; i < this.result.length; i += 2) {
					const pair = this.result.slice(i, i + 2)
					pairedPrevImgs.push(pair)
				}
				return pairedPrevImgs
			}
		},
		onReachBottom() {
			this.page += 1
			if (this.page > this.total_pages) {
				this.page -= 1
				this.loadAble = 'nomore'
			} else {
				this.loadAble = 'loading'
				this.getImg()
				this.loadAble = 'loadmore'
			}
		},
		onPullDownRefresh() {
			this.page = 1
			this.getImg()
			uni.stopPullDownRefresh()
		}
	}
</script>

<style lang="scss" scoped>
	.row {
		width: 750rpx;
		height: 100vh;

		.ImgsBox {
			display: flex;
			margin-top: 10rpx;
		}

		.Search {
			padding-top: 20rpx;
			margin-bottom: 10rpx;
			padding-left: 10rpx;
		}
	}
</style>